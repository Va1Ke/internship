from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.utils.utils import get_email_from_token
from app.config import settings
from app.schemas import quiz_workflow_schemas
from app.cruds.company_crud import crud as company_crud
from app.cruds.quiz_crud import crud as quiz_crud
from app.cruds.quiz_workflow_crud import crud as quiz_workflow_crud
from app.cruds.crud import crud as user_crud
from fastapi.responses import FileResponse
from app.database import db

router = APIRouter()

@router.post("/get-my-result-redis/", tags=["download_csv"])
async def get_my_result_redis(email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email,db=db)
    await quiz_workflow_crud.export_user_results_redis_to_csv(user_id=owner.id,db=db)
    return FileResponse("export_user_results_redis_to_csv.csv")

@router.post("/get-user-result-by-company-redis/", tags=["download_csv"])
async def get_user_result_by_company_redis(user_id: int, company_id: int, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email,db=db)
    check_is_admin = await company_crud.check_is_admin(company_id=company_id, user_id=owner.id,db=db)
    company = await company_crud.get_company_by_id(company_id,db=db)
    if company.owner_id == owner.id or check_is_admin:
        await quiz_workflow_crud.export_user_by_company_results_redis_to_csv(user_id=user_id, company_id=company_id,db=db)
        return FileResponse("export_user_by_company_results_redis_to_csv.csv")
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/get-company-result-redis/", tags=["download_csv"])
async def get_company_result_redis(company_id: int, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email,db=db)
    check_is_admin = await company_crud.check_is_admin(company_id=company_id, user_id=owner.id,db=db)
    company = await company_crud.get_company_by_id(company_id,db=db)
    if company.owner_id == owner.id or check_is_admin:
        await quiz_workflow_crud.export_company_results_redis_to_csv(company_id=company_id,db=db)
        return FileResponse("export_company_results_redis_to_csv.csv")
    else:
        raise HTTPException(status_code=400, detail="No permission")

