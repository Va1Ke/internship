from pydantic import BaseModel

class QuizReturn(BaseModel):
    id: int
    name: str
    description: str
    company_id: int
    avg_result: float
    frequency_of_passage: int

class QuizEntry(BaseModel):
    name: str
    description: str
    company_id: int

class QuizUpdateEntry(BaseModel):
    id: int
    name: str
    description: str