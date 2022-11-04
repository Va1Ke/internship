from pydantic import BaseModel
import datetime

class InvitationReturnFromCreation(BaseModel):
    id: int
    company_id: int
    status: bool
    invited_user_id: int

class InvitationAdd(BaseModel):
    company_id: int
    invited_user_id: int

class UserCompanyReturn(BaseModel):
    id: int
    company_id: int
    user_id: int
