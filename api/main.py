from fastapi import FastAPI
from pydantic import BaseModel
import math, random

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

class VerifyRequest(BaseModel):
    email_address: str
    one_time_password: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/is_verified")
async def check_verification():
    """ Returns boolean value indicating whether provided email address has
    already been verified in the database.
    """
    return False

@app.post("/verify/")
async def verify(request: VerifyRequest):
    """
    Verify an email address given the email address and OTP
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
 
    return request
