from pydantic import BaseModel
from typing import Union

class QuizReturn(BaseModel):
    id: int
    name: str
    description: str
    company_id: int
    avg_result: Union[float, None]
    frequency_of_passage: Union[int, None]

class QuizEntry(BaseModel):
    name: str
    description: str
    company_id: int

class QuizUpdateEntry(BaseModel):
    id: int
    name: str
    description: str