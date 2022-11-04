from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    name = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    creation_date = Column(DateTime)

    company = relationship("Company")

users = User.__table__


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    name = Column(String)
    description = Column(Text)
    creation_date = Column(DateTime)
    updated = Column(DateTime)
    hide = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))

companies = Company.__table__

class UserOfCompany(Base):
    __tablename__ = "users_of_companys"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    is_admin = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))

users_of_companys = UserOfCompany.__table__

class InvitationFromOwner(Base):
    __tablename__ = "invitations_from_owner"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    status = Column(Boolean, nullable=True)
    invited_user_id = Column(Integer, ForeignKey("users.id"))

invitations_from_owner = InvitationFromOwner.__table__

class RequestFromUser(Base):
    __tablename__ = "requests_from_user"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    status = Column(Boolean, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

requests_from_user = RequestFromUser.__table__