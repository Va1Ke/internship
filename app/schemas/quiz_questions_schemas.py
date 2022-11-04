from pydantic import BaseModel

class QuizQuestionReturn(BaseModel):
    id: int
    description: str
    quiz_id: int

class QuizQuestionEntry(BaseModel):
    description: str
    quiz_id: int