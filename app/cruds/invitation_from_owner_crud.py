from fastapi import HTTPException
from datetime import datetime
from app.schemas import company_schemas
from app.schemas import invitation_from_owner_schemas
from app.models.models import companies, invitations_from_owner, users_of_companys
from app.database import db
from sqlalchemy import and_

class InvitationFromOwner_crud:

    async def create_invitation(self, inventation: invitation_from_owner_schemas.InvitationAdd):
        db_company = invitations_from_owner.insert().values(company_id=inventation.company_id, invited_user_id=inventation.invited_user_id, status=False)
        record_id = await db.execute(db_company)
        #user_by_email = await db.fetch_one(companies.select().where(companies.c.email == companies.email))
        return invitation_from_owner_schemas.InvitationReturnFromCreation(**inventation.dict(), id=record_id,status=False)

    async def get_invitation_by_id(self, id: int):
        invitation = await db.fetch_one(invitations_from_owner.select().where(invitations_from_owner.c.id == id))
        if invitation == None:
            return None
        return invitation_from_owner_schemas.InvitationReturnFromCreation(**invitation)

    async def get_invitation_by_invented_id(self, id: int):
        query = invitations_from_owner.select().where(invitations_from_owner.c.invited_user_id == id)
        list_invitation = await db.fetch_all(query=query)
        if list_invitation == None:
            return None
        return [invitation_from_owner_schemas.InvitationReturnFromCreation(**invitation) for invitation in list_invitation]

    async def accept_invitation(self, invitation_id: int, company_id: int, user_id: int):
        db_company = users_of_companys.insert().values(company_id=company_id, user_id=user_id)
        record_id = await db.execute(db_company)
        await self.decline_invitation(invitation_id)
        return invitation_from_owner_schemas.UserCompanyReturn(id=record_id, company_id=company_id, user_id=user_id)

    async def delete_user_from_company(self, company_id: int, user_id: int):
        query = users_of_companys.delete().where(and_(users_of_companys.c.company_id == company_id, users_of_companys.c.user_id == user_id))
        await db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

    async def decline_invitation(self, invitation_id: int):
        query = invitations_from_owner.delete().where(invitations_from_owner.c.id == invitation_id)
        await db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")


crud = InvitationFromOwner_crud()
