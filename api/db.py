from typing import Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Mapped, Session

Base = declarative_base()

class OneTimePassword(Base):
    __tablename__ = 'otp'
    __table_args__ = {'schema': 'everify'}

    id = Column(Integer, primary_key=True)
    otp = Column(String)
    created_at = Mapped[Optional[DateTime]]
    # TODO: email_id is a foreign key to verified_email.id
    email_id = Column(Integer)
    #email_id = mapped_column(ForeignKey("verified_email.id"))

class VerifiedEmail(Base):
    __tablename__ = 'verified_email'
    __table_args__ = {'schema': 'everify'}

    id = Column(Integer, primary_key = True)
    auth_provider_uuid = Column(String)
    email_address = Column(String)
    verified_at = Column(DateTime)



def get_email_id(email_address: str, auth_provider: str, session: Session):
    """
    Returns the ID (primary key) from verified_email table that matches 
    the given email_address and auth_provider
    """
    print(email_address, auth_provider)
    # filter conditions are joined by AND operator
    result = session.query(VerifiedEmail)\
        .filter(VerifiedEmail.auth_provider_uuid == auth_provider) \
        .filter(VerifiedEmail.email_address == email_address) \
        .first()

    if result is None:
        return None
    else:
        return result.id
