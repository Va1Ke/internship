from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import and_
from app.schemas import requst_from_user_schemas, invitation_from_owner_schemas
from app.models.models import companies, requests_from_user, users_of_companys
import databases

class RequestFromUser_crud:
    def __init__(self, db: databases.Database):
        self.db = db

    async def create_request(self, company_id: int, user_id: int) -> requst_from_user_schemas.UserRequestReturn:
        db_company = requests_from_user.insert().values(company_id=company_id, user_id=user_id, status=False)
        record_id = await self.db.execute(db_company)
        return requst_from_user_schemas.UserRequestReturn(company_id=company_id, user_id=user_id, status=False, id=record_id)

    async def get_request_by_id(self, request_id: int) -> requst_from_user_schemas.UserRequestReturn:
        request = await self.db.fetch_one(requests_from_user.select().where(requests_from_user.c.id == request_id))
        if request == None:
            return None
        return requst_from_user_schemas.UserRequestReturn(**request)

    async def accept_request_from_user(self, request_id: int, company_id: int, user_id: int) -> invitation_from_owner_schemas.UserCompanyReturn:
        db_company = users_of_companys.insert().values(company_id=company_id, user_id=user_id)
        record_id = await self.db.execute(db_company)
        query = requests_from_user.delete().where(requests_from_user.c.id == request_id)
        await self.db.execute(query=query)
        return invitation_from_owner_schemas.UserCompanyReturn(id=record_id, company_id=company_id, user_id=user_id)

    async def decline_request_from_user(self, request_id: int) -> HTTPException:
        query = requests_from_user.delete().where(requests_from_user.c.id == request_id)
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

#crud = RequestFromCruds()