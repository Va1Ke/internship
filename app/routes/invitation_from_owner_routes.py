from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.utils.utils import get_email_from_token
from app.config import settings
from app.schemas.invitation_from_owner_schemas import *
import http.client
from datetime import timedelta
from app.cruds.company_crud import crud as company_crud
from app.cruds.crud import crud as user_crud
from app.cruds.invitation_from_owner_crud import crud as from_owner_crud

router = APIRouter()

@router.post("/invitation/", tags=["Invitation from owner"], response_model=InvitationReturnFromCreation)
async def create(invitation: InvitationAdd, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    company = await company_crud.get_company_by_id(invitation.company_id)
    if company.owner_id == owner.id:
        return await from_owner_crud.create_invitation(invitation)
    else:
        raise HTTPException(status_code=400,detail="No permission")


@router.get("/check-my-invitation/", tags=["Invitation from owner"], response_model=list[InvitationReturnFromCreation])
async def check(email: str = Depends(get_email_from_token)):
    invited = await user_crud.get_user_by_email(email)
    return await from_owner_crud.get_invitation_by_invented_id(invited.id)


@router.post("/accept/", tags=["Invitation from owner"], response_model=UserCompanyReturn)
async def accept(invitation_id: int, email: str = Depends(get_email_from_token)):
    invited = await user_crud.get_user_by_email(email)
    invitation = await from_owner_crud.get_invitation_by_id(invitation_id)
    if invited.id == invitation.invited_user_id:
        return await from_owner_crud.accept_invitation(invitation_id=invitation_id, company_id=invitation.company_id, user_id=invitation.invited_user_id)
    else:
        raise HTTPException(status_code=400,detail="No permission")


@router.delete("/decline/", tags=["Invitation from owner"])
async def decline(invitation_id: int, email: str = Depends(get_email_from_token)):
    invited = await user_crud.get_user_by_email(email)
    invitation = await from_owner_crud.get_invitation_by_id(invitation_id)
    if invited.id == invitation.invited_user_id:
        return await from_owner_crud.decline_invitation(invitation_id)
    else:
        raise HTTPException(status_code=400,detail="No permission")


