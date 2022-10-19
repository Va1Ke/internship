from sqlalchemy import Column,String,Integer,DateTime
from app.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    name = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    creation_date = Column(DateTime)

