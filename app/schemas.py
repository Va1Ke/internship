from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    email: str


class SignInUser(UserBase):
    password: str


class SignUpUser(UserBase):
    email: str
    name: str
    password: str

class UserUpdate(UserBase):
    name: str
    password: str

class UserList(UserBase):
    id: int
    name: str
    password: str

class User(UserBase):
    id: int
    name: str
    email: str
    password: str
    creation_date: datetime.datetime
    class Config:
        orm_mode = True