from dotenv import load_dotenv
load_dotenv()

from typing import Annotated, Optional
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import math, random
import urllib.parse
import math, random
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db import OneTimePassword, VerifiedEmail, get_email_id
import emailService
import os


description = """

Email verification system for any type of user account

You can:
* **Create a OTP for an email address**
* **Verify an account (based on auth_provider_uuid and email_address) with OTP**
* **Check whether an email address has already been verified**

"""

app = FastAPI(
    title="Email Verifier",
    description=description,
    version="0.0.1"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

PGHOST = os.getenv('PGHOST')
PGUSER = os.getenv('PGUSER')
PGPASS = os.getenv('PGPASSWORD')
PGPORT = int(os.getenv('PGPORT'))
CONNECTION_STRING= f'postgresql://{PGUSER}:{PGPASS}@{PGHOST}/everify'
engine = create_engine(CONNECTION_STRING)


class OTPRequest(BaseModel):
    email_address: str
    auth_provider_uuid: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ready")
def kubernetes_readiness_probe():
    return {"status": "healthy"}

@app.get("/live")
def kubernetes_readiness_probe():
    return {"status": "alive"}

async def root():
    return {"message": "Hello World"}

@app.get("/verify_page", response_class=HTMLResponse)
async def verify_page(request: Request, email_address: str = "missing",route_prefix: str = "", auth_provider_uuid: str = "", redirect_url="test redirect", validation_failed = ""):
    failed_valid = True if validation_failed.lower() == 'true' else False
    return templates.TemplateResponse("verify.html",
                                      {"request": request,
                                       "email_address": email_address,
                                       "redirect_url": redirect_url,
                                       "auth_provider_uuid": auth_provider_uuid,
                                       "route_prefix": route_prefix,
                                       "validation_failed": failed_valid})


@app.get("/is_verified")
async def check_verification(email_address: str, auth_provider_uuid: str):
    """
    @param email_address: string
    @param auth_provider_uuid: string identifier of account given by the auth provider (in OAuth token)

    Params are passed as query params in URL.

    Returns boolean value indicating whether provided email address has
    already been verified in the database.
    """


    with Session(engine) as session:
        email_id = get_email_id(email_address, auth_provider=auth_provider_uuid, session=session)

        print('email_id: {}'.format(email_id))
        r = Response()

        if email_id is None:
            r.status_code = 401
            return r

        exists = session.query(VerifiedEmail)\
            .filter(VerifiedEmail.id == email_id, VerifiedEmail.verified_at.isnot(None))\
            .first()

        r.status_code = 200 if exists else 401
        return r


@app.post("/verify")
async def verify(email_address: Annotated[str, Form()],
                 one_time_password: Annotated[str, Form()],
                 redirect_url: Annotated[str, Form()],
                 auth_provider_uuid: Annotated[str, Form()]):
    print(email_address)
    print(one_time_password)
    print(redirect_url)
    print(auth_provider_uuid)
    """
    Verify an email address given the OTP and ID of the record
    """
    with Session(engine) as session:
        email_id = get_email_id(email_address, auth_provider=auth_provider_uuid, session=session)

        print('email_id: {}'.format(email_id))

        password_results = session.query(OneTimePassword)\
            .where(OneTimePassword.otp == one_time_password)\
            .where(OneTimePassword.email_id == email_id)\
            .all()

        print('password_results: {}'.format(password_results))

        # TODO: also want logic for checking expiry of OTP

        # TODO: will want to check whether email has already been verified instead of verifying again

        if password_results is not None and len(password_results) > 0:
            verified_email_record = session.query(VerifiedEmail)\
                .where(VerifiedEmail.id == email_id).first()
            print('verified_email_record: {}'.format(verified_email_record))
            verified_email_record.verified_at = datetime.datetime.now()

            session.add(verified_email_record)
            session.commit()

            # validation succeeded
            return Response(status_code=200)

        else:
            # validation failed
            return Response(status_code=401)


@app.post("/create_otp/")
async def generate_otp(request: OTPRequest):
    """
    Generate a one time passcode given the email address and auth provider
    """

    digits = "0123456789"
    password = ""

    #length of password can be changed by changing value in range
    for _ in range(4) :
        password += digits[math.floor(random.random() * 10)]

    with Session(engine) as session:

        #TODO check if email and authprovider already match
        exist = session.query(VerifiedEmail).filter(
            VerifiedEmail.email_address.match(request.email_address), 
            VerifiedEmail.auth_provider_uuid.match(request.auth_provider_uuid), 
            VerifiedEmail.verified_at.isnot(None)).first()
        if exist:
            print(exist.id, exist.email_address)
            raise HTTPException(
                status_code=400, detail="email already exists")
        else:
            print('Creating new VerifiedEmail record...')

        y = VerifiedEmail(auth_provider_uuid = request.auth_provider_uuid, email_address = request.email_address)
        session.add(y)

        session.commit()
        session.refresh(y)

        print(y.id)

        x = OneTimePassword(email_id = y.id, otp = password)

        session.add(x)
        session.commit()

        # send otp to user
        email = emailService.EmailService()
        emailResponse = email.send_email(request.email_address, password)

    return emailResponse
