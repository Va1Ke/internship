from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.utils.utils import get_email_from_token
from app.config import settings
from app.schemas import quiz_workflow_schemas
from app.cruds.company_crud import Company_crud
from app.cruds.quiz_crud import Quiz_crud
from app.cruds.quiz_workflow_crud import QuizWorkFlow_crud
from app.cruds.crud import Cruds
from fastapi.responses import FileResponse
from app.database import db, test_db


router = APIRouter()

@router.post("/get-my-result-redis/", tags=["download_csv"])
async def get_my_result_redis(email: str = Depends(get_email_from_token)):
    owner = await Cruds(db=db).get_user_by_email(email)
    await QuizWorkFlow_crud(db=db).export_user_results_redis_to_csv(user_id=owner.id)
    return FileResponse("export_user_results_redis_to_csv.csv")

@router.post("/get-user-result-by-company-redis/", tags=["download_csv"])
async def get_user_result_by_company_redis(user_id: int, company_id: int, email: str = Depends(get_email_from_token)):
    owner = await Cruds(db=db).get_user_by_email(email)
    check_is_admin = await Company_crud(db=db).check_is_admin(company_id=company_id, user_id=owner.id)
    company = await Company_crud(db=db).get_company_by_id(company_id)
    if company.owner_id == owner.id or check_is_admin:
        await QuizWorkFlow_crud(db=db).export_user_by_company_results_redis_to_csv(user_id=user_id, company_id=company_id)
        return FileResponse("export_user_by_company_results_redis_to_csv.csv")
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/get-company-result-redis/", tags=["download_csv"])
async def get_company_result_redis(company_id: int, email: str = Depends(get_email_from_token)):
    owner = await Cruds(db=db).get_user_by_email(email)
    check_is_admin = await Company_crud(db=db).check_is_admin(company_id=company_id, user_id=owner.id)
    company = await Company_crud(db=db).get_company_by_id(company_id)
    if company.owner_id == owner.id or check_is_admin:
        await QuizWorkFlow_crud(db=db).export_company_results_redis_to_csv(company_id=company_id)
        return FileResponse("export_company_results_redis_to_csv.csv")
    else:
        raise HTTPException(status_code=400, detail="No permission")

