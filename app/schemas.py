from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    email: str


class SignInUser(UserBase):
    password: str

class SignUpUser(UserBase):
    name: str
    password: str

class UserDelete(UserBase):
    password: str

class UserUpdate(UserBase):
    id: int
    name: str
    password: str

class User(UserBase):
    id: int
    name: str
    password: str
    creation_date: datetime.datetime

class UserList(UserBase):
    id: int
    name: str
    users: list[User]
    creation_date: datetime.datetime
