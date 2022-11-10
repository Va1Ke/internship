from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.utils.utils import get_email_from_token
from app.config import settings
from app.schemas.requst_from_user_schemas import *
import http.client
from datetime import timedelta
from app.cruds.company_crud import Company_crud
from app.cruds.crud import UserCrud
from app.cruds.request_from_user_crud import RequestFromUser_crud
from app.database import db, test_db

router = APIRouter()

@router.post("/create-request/", tags=["Request from user"], response_model=UserRequestReturn)
async def create(company_id: int, email: str = Depends(get_email_from_token)):
    user = await UserCrud(db=db).get_user_by_email(email)
    return await RequestFromUser_crud(db=db).create_request(company_id=company_id, user_id=user.id)

@router.delete("/delete-request/", tags=["Request from user"])
async def delete_request(request_id: int, email: str = Depends(get_email_from_token)):
    user = await UserCrud(db=db).get_user_by_email(email)
    request = await RequestFromUser_crud(db=db).get_request_by_id(request_id=request_id)
    company = await Company_crud(db=db).get_company_by_id(company_id=request.company_id)
    if company.owner_id == user.id:
        return await RequestFromUser_crud(db=db).decline_request_from_user(request_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")
