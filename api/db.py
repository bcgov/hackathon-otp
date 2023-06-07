from typing import Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Mapped

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



async def get_email_id(email_address: str, auth_provider: str, session: Session):
    """
    Returns the ID (primary key) from verified_email table that matches 
    the given email_address and auth_provider
    """
    results = session.select(VerifiedEmail).where(VerifiedEmail.email_address.match(email_address)).where(VerifiedEmail.auth_provider_uuid.match(auth_provider)).first()
    return results.id