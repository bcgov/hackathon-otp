from fastapi import FastAPI
from pydantic import BaseModel
import math, random
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import Session, mapped_column
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

engine = create_engine('')

Base = declarative_base()

class OneTimePassword(Base):
    __tablename__ = 'otp'

    id = Column(Integer, primary_key=True)
    otp = Column(String)
    created_at = Column(DateTime)
    email_id = mapped_column(ForeignKey("verified_email.id"))

class VerifiedEmail(Base):
    __tablename__ = 'verified_email'

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
