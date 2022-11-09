from pydantic import BaseModel
import datetime

class UserResult(BaseModel):
    avg: float
    time: datetime.datetime

class UserQuizList(BaseModel):
    quiz_id: int
    time: datetime.datetime

class ListUsersOfCompanyAndLastTime(BaseModel):
    user_id: int
    time: datetime.datetime

