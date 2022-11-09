from pydantic import BaseModel
import datetime

class QuizWorkFlowQuestionsReturn(BaseModel):
    id: int
    description: str
    quiz_id: int

class QuizWorkFlowReturn(BaseModel):
    id: int
    user_id: int
    company_id: int
    quiz_id: int
    result: float
    right_answers: int
    count_of_questions: int
    time: datetime.datetime

class QuestionAnswer(BaseModel):
    question_id: int
    answer: str

class QuizWorkFlowEntering(BaseModel):
    answers: list[QuestionAnswer]