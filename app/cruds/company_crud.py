from fastapi import HTTPException
from datetime import datetime
import databases
from sqlalchemy import and_
from app.schemas import company_schemas, requst_from_user_schemas, user_of_company_schemas
from app.models.models import companies, requests_from_user, users_of_companys

class Company_crud:

    async def create_company(self, company: company_schemas.Company, owner_id: int, db: databases.Database) -> company_schemas.CompanyReturn:
        db_company = companies.insert().values(name=company.name, description=company.description, owner_id=owner_id, creation_date=company.creation_date, updated=company.updated, hide=company.hide)
        record_id = await db.execute(db_company)
        #user_by_email = await db.fetch_one(companies.select().where(companies.c.email == companies.email))
        return company_schemas.CompanyReturn(**company.dict(), id=record_id, owner_id=owner_id)


    async def add_to_admins_in_company(self, company_id: int, user_id: int, db: databases.Database) -> user_of_company_schemas.UserOfCompanyReturn:
        query = (users_of_companys.update().where(and_(users_of_companys.c.company_id == company_id, users_of_companys.c.user_id == user_id)).values(
            is_admin=True
        ).returning(users_of_companys.c.id))
        record_id = await db.execute(query=query)
        return user_of_company_schemas.UserOfCompanyReturn(id=record_id, company_id=company_id, user_id=user_id, is_admin=True)

    async def check_is_admin(self, company_id: int, user_id: int) -> bool:
        query = users_of_companys.select().where(and_(users_of_companys.c.company_id == company_id, users_of_companys.c.user_id == user_id))
        returned = await db.fetch_one(query=query)
        if returned == None:
            return False
        user = user_of_company_schemas.UserOfCompanyReturn(**returned)
        if user.is_admin == True:
            return True
        else:
            return False

    async def check_is_user_in_company(self, company_id: int, user_id: int, db: databases.Database) -> bool:
        query = users_of_companys.select().where(and_(users_of_companys.c.company_id == company_id, users_of_companys.c.user_id == user_id))
        returned = await db.fetch_one(query=query)
        if returned:
            return bool(True)
        else:
            return bool(False)

    async def get_company(self, owner_id, db: databases.Database) -> list[company_schemas.CompanyReturn]:
        query = companies.select().where(companies.c.owner_id == owner_id)
        list_companies = await db.fetch_all(query=query)
        if list_companies == None:
            return None
        return [company_schemas.CompanyReturn(**company) for company in list_companies]

    async def show_requests_from_users(self, company_id: int, db: databases.Database) -> list:
        query = requests_from_user.select().where(requests_from_user.c.company_id == company_id)
        list = await db.fetch_all(query=query)
        if list == None:
            return None
        return [requst_from_user_schemas.UserRequestReturn(**request) for request in list]

    async def get_companies(self, db: databases.Database) -> list[company_schemas.CompanyReturn]:
        query = companies.select().where(companies.c.hide == False)
        list_companies = await db.fetch_all(query=query)
        if list_companies == None:
            return None
        return [company_schemas.CompanyReturn(**company) for company in list_companies]

    async def get_company_by_id(self, company_id, db: databases.Database) -> company_schemas.CompanyReturn:
        company = await db.fetch_one(companies.select().where(companies.c.id == company_id))
        if company == None:
            return None
        return company_schemas.CompanyReturn(**company)

    async def update_company(self, company: company_schemas.UpdateCompany, db: databases.Database) -> company_schemas.CompanyReturn:
        query = (companies.update().where(companies.c.id == company.id).values(
        name=company.name,
        description=company.description,
        hide=company.hide,
        updated=company.updated
        ).returning(companies.c.owner_id))
        owner_id = await db.execute(query=query)
        return company_schemas.CompanyReturn(**company.dict(), owner_id=owner_id)

    async def delete_company(self, id: int, db: databases.Database) -> HTTPException:
        query = companies.delete().where(companies.c.id == id)
        await db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

    async def delete_user_from_company(self, user_id: int, company_id: int, db: databases.Database) -> HTTPException:
        query = users_of_companys.delete().where(and_(users_of_companys.c.company_id == company_id, users_of_companys.c.user_id == user_id))
        await db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

crud = Company_crud()
