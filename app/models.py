from sqlalchemy import Column,String,Integer,DateTime
from app.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    name = Column(String)
    email = Column(String, unique=True)
    date = Column(DateTime)

