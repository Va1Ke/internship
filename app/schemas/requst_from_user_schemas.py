from pydantic import BaseModel
import datetime

class UserRequestReturn(BaseModel):
    id: int
    company_id: int
    status: bool
    user_id: int

class UserRequest(BaseModel):
    company_id: int