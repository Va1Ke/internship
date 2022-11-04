from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.utils.utils import get_email_from_token
from app.config import settings
from app.schemas.company_schemas import *
import http.client
from datetime import timedelta
from app.cruds.company_crud import crud as company_crud
from app.cruds.request_from_user_crud import crud as req_from_user_crud
from app.cruds.crud import crud as user_crud

router = APIRouter()

@router.post("/create-company/", tags=["company"])
async def create(company: Company, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    return await company_crud.create_company(company=company, owner_id=owner.id)

@router.post("/add-to-admins/", tags=["company"])
async def create(company_id: int, user_id: int, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    company = await company_crud.get_company_by_id(company_id)
    if company.owner_id == owner.id:
        return await company_crud.add_to_admins_in_company(company_id=company_id, user_id=user_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/show-requests-from-users/", tags=["company"])
async def create(company_id: int, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    company = await company_crud.get_company_by_id(company_id)
    if company.owner_id == owner.id:
        return await company_crud.show_requests_from_users(company_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/accept-request-from-user/", tags=["company"])
async def accept_request_from_user(request_id: int, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    request = await req_from_user_crud.get_request_by_id(request_id)
    company = await company_crud.get_company_by_id(request.company_id)
    if company.owner_id == owner.id:
        return await req_from_user_crud.accept_request_from_user(request_id=request_id, company_id=company.id, user_id=request.user_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.put("/update-company/", tags=["company"])
async def update(company: UpdateCompany, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    company_get = await company_crud.get_company_by_id(company.id)
    if company_get.owner_id == owner.id:
        return await company_crud.update_company(company=company)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.delete("/delete-company/", tags=["company"])
async def delete(company_id: int, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    company = await company_crud.get_company_by_id(company_id)
    if company.owner_id == owner.id:
        return await company_crud.delete_user_from_company()
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.delete("/delete-user-from-company/", tags=["company"])
async def delete_user(company_id: int, user_id: int, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    company = await company_crud.get_company_by_id(company_id)
    if company.owner_id == owner.id:
        return await company_crud.delete_user_from_company(company_id=company_id,user_id=user_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/get-company-by-owner/", tags=["company"])
async def get_company_by_owner(email: str = Depends(get_email_from_token)):
    user_exist = await user_crud.get_user_by_email(email)
    if user_exist:
        return await company_crud.get_company(user_exist.id)
    else:
        raise HTTPException(status_code=400, detail="No such user")

@router.post("/show-companies/", tags=["company"])
async def show_companies():
    return await company_crud.get_companies()
