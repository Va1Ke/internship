from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.utils.utils import get_email_from_token
from app.config import settings
from app.schemas.company_schemas import *
import http.client
from datetime import timedelta
from app.schemas import analitics_schemas
from app.cruds.company_crud import Company_crud
from app.cruds.quiz_crud import Quiz_crud
from app.cruds.quiz_workflow_crud import QuizWorkFlow_crud
from app.cruds.crud import Cruds
from app.database import db, test_db

router = APIRouter()

@router.post("/get-all-user-result/", tags=["analytics"], response_model=list[analitics_schemas.UserResult])
async def get_all_user_results(user_id: int) -> list[analitics_schemas.UserResult]:
        return await Quiz_crud(db=db).show_result_of_user(user_id)


@router.post("/get-results-by-company-and-user/", tags=["analytics"], response_model=list[analitics_schemas.UserResult])
async def get_by_company_and_users(company_id: int, user_id: int, email: str = Depends(get_email_from_token)) -> list[analitics_schemas.UserResult]:
    owner = await Cruds(db=db).get_user_by_email(email)
    company = await Company_crud(db=db).get_company_by_id(company_id)
    check_is_admin = await Company_crud(db=db).check_is_admin(company_id=company_id, user_id=owner.id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await Quiz_crud(db=db).show_all_result_by_company_and_user(company_id=company_id, user_id=user_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/get-list-user-of-company-and-last_time/", tags=["analytics"], response_model=list[analitics_schemas.ListUsersOfCompanyAndLastTime])
async def get_by_company_and_users(company_id: int, email: str = Depends(get_email_from_token)) -> list[analitics_schemas.ListUsersOfCompanyAndLastTime]:
    owner = await Cruds(db=db).get_user_by_email(email)
    company = await Company_crud(db=db).get_company_by_id(company_id)
    check_is_admin = await Company_crud(db=db).check_is_admin(company_id=company_id, user_id=owner.id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await Quiz_crud(db=db).list_user_of_company_and_last_time(company_id=company_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/get-users-result-by-company/", tags=["analytics"], response_model=list[analitics_schemas.UserResult])
async def get_user_result(company_id: int) -> list[analitics_schemas.UserResult]:
    return await Quiz_crud(db=db).show_all_result_by_company(company_id=company_id)

@router.post("/get-quiz-result/", tags=["analytics"], response_model=list[analitics_schemas.UserResult])
async def get_quiz_result(quiz_id: int, user_id: int) -> list[analitics_schemas.UserResult]:
    return await Quiz_crud(db=db).show_quiz_result_by_user(quiz_id=quiz_id, user_id=user_id)

@router.post("/get-quiz-time/", tags=["analytics"], response_model=list[analitics_schemas.UserQuizList])
async def get_quiz_time(user_id: int) -> list[analitics_schemas.UserQuizList]:
    return await Quiz_crud(db=db).show_user_quiz_list(user_id=user_id)


