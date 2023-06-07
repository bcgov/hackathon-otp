from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math, random, json
import urllib.parse
import math, random
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import emailService 
from typing import Annotated
import urllib.parse

description = """

Email verification system for Basic BCeID accounts

You can:
* **Create a OTP for an email address** (_not implemented_)
* **Check whether an email address has already been verified** (_not implemented_)

"""

app = FastAPI(
    title="Email Verifier",
    description=description,
    version="0.0.1"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

engine = create_engine('postgresql://awilliam@localhost:5432/email_verification')

Base = declarative_base()

class OneTimePassword(Base):
    __tablename__ = 'otp'
    __table_args__ = {'schema': 'everify'}

    id = Column(Integer, primary_key=True)
    otp = Column(String)
    created_at = Mapped[Optional[DateTime]]
    email_id = Column(Integer)
    #email_id = mapped_column(ForeignKey("verified_email.id"))

class VerifiedEmail(Base):
    __tablename__ = 'verified_email'
    __table_args__ = {'schema': 'everify'}

    id = Column(Integer, primary_key = True)
    auth_provider_uuid = Column(Integer)
    email_address = Column(String)
    verified_at = Column(DateTime)

class VerifyRequest(BaseModel):
    email_address: str
    one_time_password: str
    redirect_url: str

class RequestToVerify(BaseModel):
    email_id: Optional[int]
    one_time_password: str
    email_address: str
    auth_provider_uuid: str

class OTPRequest(BaseModel):
    email_address: str
    auth_provider_uuid: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/verify_page", response_class=HTMLResponse)
async def verify_page(request: Request, email_address: str = "missing", redirect_url="test redirect"):
    return templates.TemplateResponse("verify.html", 
                                      {"request": request, 
                                       "email_address": email_address, 
                                       "redirect_url": urllib.parse.quote(email_address),
                                       "validation_failed": False})
   

@app.get("/is_verified")
async def check_verification(id: int):
    """ Returns boolean value indicating whether provided email address has
    already been verified in the database.
    """

    with Session(engine) as session:
        exist = session.select(VerifiedEmail).where(VerifiedEmail.id.match(id)).where(VerifiedEmail.verified_at.is_not(None)).first()
        if exist:
            return True
        else:
            return False

@app.post("/verify")
async def verify(email_address: Annotated[str, Form()], 
                 one_time_password: Annotated[str, Form()], 
                 redirect_url: Annotated[str, Form()]):
    print(email_address)
    print(one_time_password)
    print(redirect_url)
    """
    Verify an email address given the OTP and ID of the record
    """
    with Session(engine) as session:
        email_id = get_email_id(email_address, auth_provider='1', session=session)
        
        session.query(VerifiedEmail)\
            .where()

        # If validation succeeds
        return RedirectResponse(urllib.parse.unquote(redirect_url))

        # If validation fails
        return templates.TemplateResponse("verify.html", {"request": {}, 
                                                      "email_address": email_address,
                                                      "validation_failed": True})
@app.post("/create_otp/")
async def generate_otp(request: OTPRequest):
    """
    Generate a one time passcode given the email address and auth provider
    """

    digits = "0123456789"
    password = ""
 
    #length of password can be changed by changing value in range
    for i in range(4) :
        password += digits[math.floor(random.random() * 10)]

    with Session(engine) as session:

        #TODO check if email and authprovider already match
        exist = session.query(VerifiedEmail).filter(
            VerifiedEmail.email_address == request.email_address, VerifiedEmail.auth_provider_uuid == request.auth_provider_uuid).first()
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

    return request
