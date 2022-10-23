from sqlalchemy import Column,String,Integer,DateTime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    name = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    creation_date = Column(DateTime)

    def __init__(self,name,password,email,creation_date):
        self.name = name
        self.password = password
        self.email = email
        self.creation_date = creation_date

users=User.__table__