from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.utils.utils import get_email_from_token
from app.config import settings
from app.schemas.company_schemas import *
import http.client
from datetime import timedelta
from app.schemas import company_schemas, requst_from_user_schemas, user_of_company_schemas, invitation_from_owner_schemas
from app.cruds.company_crud import Company_crud
from app.cruds.request_from_user_crud import RequestFromUser_crud
from app.cruds.crud import UserCrud
from app.database import db, test_db

router = APIRouter()

@router.post("/create-company/", tags=["company"], response_model=company_schemas.CompanyReturn)
async def create(company: Company, email: str = Depends(get_email_from_token)):
    owner = await UserCrud(db=db).get_user_by_email(email)
    return await Company_crud(db=db).create_company(company=company, owner_id=owner.id)

@router.post("/add-to-admins/", tags=["company"], response_model=user_of_company_schemas.UserOfCompanyReturn)
async def add_admins(company_id: int, user_id: int, email: str = Depends(get_email_from_token)):
    owner = await UserCrud(db=db).get_user_by_email(email)
    company = await Company_crud(db=db).get_company_by_id(company_id)
    if company.owner_id == owner.id:
        return await Company_crud(db=db).add_to_admins_in_company(company_id=company_id, user_id=user_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")


@router.post("/show-requests-from-users/", tags=["company"], response_model=list[requst_from_user_schemas.UserRequestReturn])
async def show_requests_from_users(company_id: int, email: str = Depends(get_email_from_token)):
    owner = await UserCrud(db=db).get_user_by_email(email)
    company = await Company_crud(db=db).get_company_by_id(company_id)
    if company.owner_id == owner.id:
        return await Company_crud(db=db).show_requests_from_users(company_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/accept-request-from-user/", tags=["company"], response_model=invitation_from_owner_schemas.UserCompanyReturn)
async def accept_request_from_user(request_id: int, email: str = Depends(get_email_from_token)):
    owner = await UserCrud(db=db).get_user_by_email(email)
    request = await RequestFromUser_crud(db=db).get_request_by_id(request_id)
    company = await Company_crud(db=db).get_company_by_id(request.company_id)
    if company.owner_id == owner.id:
        return await RequestFromUser_crud(db=db).accept_request_from_user(request_id=request_id, company_id=company.id, user_id=request.user_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.put("/update-company/", tags=["company"], response_model=company_schemas.CompanyReturn)
async def update(company: UpdateCompany, email: str = Depends(get_email_from_token)):
    owner = await UserCrud(db=db).get_user_by_email(email)
    company_get = await Company_crud(db=db).get_company_by_id(company.id)
    if company_get.owner_id == owner.id:
        return await Company_crud(db=db).update_company(company=company)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.delete("/delete-company/", tags=["company"])
async def delete(company_id: int, email: str = Depends(get_email_from_token)):
    owner = await UserCrud(db=db).get_user_by_email(email)
    company = await Company_crud(db=db).get_company_by_id(company_id)
    if company.owner_id == owner.id:
        return await Company_crud(db=db).delete_company(company_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.delete("/delete-user-from-company/", tags=["company"])
async def delete_user(company_id: int, user_id: int, email: str = Depends(get_email_from_token)):
    owner = await UserCrud(db=db).get_user_by_email(email)
    company = await Company_crud(db=db).get_company_by_id(company_id)
    if company.owner_id == owner.id:
        return await Company_crud(db=db).delete_user_from_company(company_id=company_id, user_id=user_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/get-company-by-owner/", tags=["company"], response_model=list[company_schemas.CompanyReturn])
async def get_company_by_owner(email: str = Depends(get_email_from_token)):
    user_exist = await UserCrud(db=db).get_user_by_email(email)
    if user_exist:
        return await Company_crud(db=db).get_company(user_exist.id)
    else:
        raise HTTPException(status_code=400, detail="No such user")

@router.post("/show-companies/", tags=["company"], response_model=list[company_schemas.CompanyReturn])
async def show_companies():
    return await Company_crud(db=db).get_companies()
