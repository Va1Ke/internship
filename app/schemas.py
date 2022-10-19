from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    email: str


class SignInUser(UserBase):
    password: str

class SignUpUser(UserBase):
    name: str
    password: str

class UserUpdate(UserBase):
    password: str


class User(UserBase):
    id: int
    name: str
    creation_date: datetime.datetime

    class Config:
        orm_mode = True

class UserList(UserBase):
    id: int
    name: str
    users: list[User]
    creation_date: datetime.datetime
