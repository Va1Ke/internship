from pydantic import BaseModel

class QuizQuestionAnswerReturn(BaseModel):
    id: int
    answer: str
    question_id: int

class QuizQuestionAnswerEntry(BaseModel):
    answer: str
    question_id: int