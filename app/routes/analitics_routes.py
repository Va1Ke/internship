from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.utils.utils import get_email_from_token
from app.config import settings
from app.schemas.company_schemas import *
import http.client
from datetime import timedelta
from app.schemas import analitics_schemas
from app.cruds.company_crud import crud as company_crud
from app.cruds.quiz_crud import crud as quiz_crud
from app.cruds.quiz_workflow_crud import crud as quiz_workflow_crud
from app.cruds.crud import crud as user_crud

router = APIRouter()

@router.post("/get-all-user-result/", tags=["analytics"], response_model=list[analitics_schemas.UserResult])
async def get_all_user_results(user_id: int):
        return await quiz_crud.show_result_of_user(user_id)


@router.post("/get-results-by-company-and-user/", tags=["analytics"], response_model=list[analitics_schemas.UserResult])
async def get_by_company_and_users(company_id: int, user_id: int, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    company = await company_crud.get_company_by_id(company_id)
    check_is_admin = await company_crud.check_is_admin(company_id=company_id, user_id=owner.id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await quiz_crud.show_all_result_by_company_and_user(company_id=company_id, user_id=user_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/get-list-user-of-company-and-last_time/", tags=["analytics"], response_model=list[analitics_schemas.ListUsersOfCompanyAndLastTime])
async def get_by_company_and_users(company_id: int, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    company = await company_crud.get_company_by_id(company_id)
    check_is_admin = await company_crud.check_is_admin(company_id=company_id, user_id=owner.id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await quiz_crud.list_user_of_company_and_last_time(company_id=company_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/get-user-result/", tags=["analytics"])
async def get_user_result(company_id: int):
    return await quiz_crud.show_all_result_by_company(company_id=company_id)

@router.post("/get-quiz-result/", tags=["analytics"])
async def get_quiz_result(quiz_id: int, user_id: int):
    return await quiz_crud.show_quiz_result_by_user(quiz_id=quiz_id, user_id=user_id)

@router.post("/get-quiz-time/", tags=["analytics"])
async def get_quiz_time(user_id: int):
    return await quiz_crud.show_user_quiz_list(user_id=user_id)
