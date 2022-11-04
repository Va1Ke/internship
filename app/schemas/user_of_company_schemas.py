from pydantic import BaseModel
import datetime

class UserOfCompanyReturn(BaseModel):
    id: int
    company_id: int
    is_admin: bool
    user_id: int