from pydantic import BaseModel
import datetime

class CompanyReturn(BaseModel):
    id: int
    name: str
    description: str
    creation_date: datetime.datetime = datetime.datetime.now()
    updated: datetime.datetime = datetime.datetime.now()
    hide: bool = False
    owner_id: int

class Company(BaseModel):
    name: str
    description: str
    creation_date: datetime.datetime = datetime.datetime.now()
    updated: datetime.datetime = datetime.datetime.now()
    hide: bool = False

class UpdateCompany(BaseModel):
    id: int
    name: str
    description: str
    hide: bool = False
    updated: datetime.datetime = datetime.datetime.now()
