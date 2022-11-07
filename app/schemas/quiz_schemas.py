from pydantic import BaseModel

class QuizReturn(BaseModel):
    id: int
    name: str
    description: str
    company_id: int

class QuizEntry(BaseModel):
    name: str
    description: str
    company_id: int

class QuizUpdateEntry(BaseModel):
    id: int
    name: str
    description: str