from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app import models, schemas

class Cruds:
    def get_user(self,db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()

    def get_users(self,db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()

    def get_user_by_email(db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    def create_user(self,db: Session, user: schemas.SignUpUser):
        #fake_hashed_password = user.password + "notreallyhashed"
        db_user = models.User(email=user.email, password=user.password,name=user.name, creation_date=datetime.now())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(self,db: Session, user: schemas.UserUpdate):
        #fake_hashed_password = user.password + "notreallyhashed"
        Object = db.query(models.User).filter(models.User.email == user.email).first()
        db.delete(Object)
        db.commit()
        return HTTPException(status_code=200, detail="User deleted successfully")

    def update_user(self,db: Session, user: schemas.UserUpdate):
        usernew = self.get_user(db, user.id)
        usernew.name = user.name
        usernew.password = user.password
        usernew.email = user.email
        db.commit()
        db.refresh(usernew)
        return user




