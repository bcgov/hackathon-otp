from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import math, random, json
import urllib.parse
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
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

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
    redirect_url: str

class RequestToVerify(BaseModel):
    email_id: int
    one_time_password: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/verify_page", response_class=HTMLResponse)
async def verify_page(request: Request, email_address: str = "missing", redirect_url="test redirect"):
    return templates.TemplateResponse("verify.html", 
                                      {"request": request, 
                                       "email_address": email_address, 
                                       "redirect_url": urllib.parse.quote(email_address)
                                       "validation_failed": False})
   

@app.get("/is_verified")
async def check_verification():
    """ Returns boolean value indicating whether provided email address has
    already been verified in the database.
    """
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
    

    """
    Declare a digits variable which stores all digits
    """
    digits = "0123456789"
    otp = ""
 
    """
    length of password can be changed by changing value in range
    """
    for i in range(4) :
        otp += digits[math.floor(random.random() * 10)]

    # If validation succeeds
    return RedirectResponse(urllib.parse.unquote(redirect_url))
 
    # If validation fails
    return templates.TemplateResponse("verify.html", {"request": {}, 
                                                      "email_address": email_address,
                                                      "validation_failed": True})
