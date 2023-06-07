from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math, random
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

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

engine = create_engine('postgresql://awilliam@localhost:5432/email_verification')

Base = declarative_base()

class OneTimePassword(Base):
    __tablename__ = 'otp'
    __table_args__ = {'schema': 'everify'}

    id = Column(Integer, primary_key=True)
    otp = Column(String)
    created_at = Column(DateTime)
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

class RequestToVerify(BaseModel):
    email_id: int
    one_time_password: str

class OTPRequest(BaseModel):
    email_address: str
    auth_provider_uuid: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

async def get_email_id(email_address: str, auth_provider: str):
    """
    Returns the ID (primary key) from verified_email table that matches 
    the given email_address and auth_provider
    """
    with Session(engine) as session:
        results = session.select(VerifiedEmail).where(VerifiedEmail.email_address.match(email_address)).where(VerifiedEmail.auth_provider_uuid.match(auth_provider)).all()



@app.get("/is_verified")
async def check_verification():
    """ Returns boolean value indicating whether provided email address has
    already been verified in the database.
    """
    return False

@app.post("/verify/")
async def verify(request: RequestToVerify):
    """
    Verify an email address given the OTP and ID of the record
    """
 
    return request

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
        print(exist.id, exist.email_address)
        if exist:
            raise HTTPException(
                status_code=400, detail="email already exists")

        y = VerifiedEmail(auth_provider_uuid = request.auth_provider_uuid, email_address = request.email_address)
        session.add(y)

        session.commit()
        session.refresh(request)

        x = OneTimePassword(email_id = request.id, otp = password)

        session.add(x)
        session.commit()

        send_email(request.email_address, password)

    return request
