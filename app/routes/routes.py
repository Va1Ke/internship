from fastapi import APIRouter
from app.utils.utils import create_access_token, get_current_user, set_up, get_email_from_token
from fastapi import Depends, HTTPException
from app.config import settings
from app.schemas.schemas import *
import http.client
from datetime import timedelta
from app.cruds.crud import crud

router = APIRouter()

@router.post("/users/",response_model=User)
async def create_user(user: SignUpUser):
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user=user)

@router.put("/update-user/",response_model=User)
async def update_user(user: UserUpdate, email: str = Depends(get_email_from_token)):
    if user.email == email:
        return await crud.update_user(user=user)
    else:
        raise HTTPException(status_code=400, detail="No such user or you have no permissions to do that")

@router.get("/users/", response_model=list[User])
async def read_users(skip: int = 0, limit: int = 100):
    return await crud.get_users(skip=skip, limit=limit)

@router.delete("/delete-user/")
async def delete_user(user: UserBase, email: str = Depends(get_email_from_token)):
    if user.email == email:
        return await crud.delete_user(user=user)
    else:
        raise HTTPException(status_code=400, detail="No such user or you have no permissions to do that")

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    db_user = await crud.get_user_by_id(id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="No such user")
    return db_user

@router.get("/users/email/{user_email}")
async def read_user_by_email(user_email: str):
    db_user = await crud.get_user_by_email(email=user_email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="No such user")
    return db_user



@router.get("/user/login/me", tags=["auth"])
def get_me(user: User = Depends(get_current_user)):
    return user

@router.post("/user/login/", tags=["auth"])
async def sign_in_my(user: SignInUser):
    user_check = await crud.get_user_by_email(user.email)
    if user_check and user_check.password == user.password:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = await create_access_token(user.email,expires_delta=access_token_expires)
        return token
    else:
        raise HTTPException(status_code=400,detail="No such user or incorrect email, password")

@router.post("/user/register/", tags=["auth"])
async def sign_up_my(user: SignUpUser):
    does_exist = await crud.get_user_by_email(email=user.email)
    if does_exist:
        raise HTTPException(status_code=400,detail="Email already registered")
    config = set_up()
    conn = http.client.HTTPSConnection(config['DOMAIN'])
    pyload="{" \
            f"\"client_id\":\"{config['CLIENT_ID']}\"," \
            f"\"client_secret\":\"{config['CLIENT_SECRET']}\"," \
            f"\"audience\":\"{config['API_AUDIENCE']}\"," \
            f"\"email\":\"{user.email}\"," \
            f"\"password\":\"{user.password}\"," \
            f"\"connection\":\"{config['CONNECTION']}\"," \
            f"\"grant_type\":\"client_credentials\"" \
           "}"
    headers = {"content-type":"application/json"}
    conn.request("POST", "/dbconnections/signup", pyload, headers)
    conn.getresponse()

    user = await crud.create_user(user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = await create_access_token(user.email,expires_delta=access_token_expires)
    return token



