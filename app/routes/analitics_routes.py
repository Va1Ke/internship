from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.utils.utils import get_email_from_token
from app.config import settings
from app.schemas.company_schemas import *
import http.client
from datetime import timedelta
from app.schemas import company_schemas, user_of_company_schemas, quiz_workflow_schemas
from app.cruds.company_crud import crud as company_crud
from app.cruds.quiz_crud import crud as quiz_crud
from app.cruds.quiz_workflow_crud import crud as quiz_workflow_crud
from app.cruds.crud import crud as user_crud

router = APIRouter()

@router.post("/get-user-result/", tags=["analytics"])
async def get_user_questions(user_id: int):
    return await quiz_crud.show_result_of_user(user_id)

@router.post("/get-quiz-result/", tags=["analytics"])
async def get_quiz_questions(quiz_id: int, user_id: int):
    return await quiz_crud.show_quiz_result_by_user(quiz_id=quiz_id, user_id=user_id)

@router.post("/get-quiz-time/", tags=["analytics"])
async def get_quiz_time(user_id: int):
    return await quiz_crud.show_user_quiz_list(user_id=user_id)
