from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/auth")


@router.post("/login")
def read_item(pd_user: schemas.UserPD, db: Session = Depends(get_db)):
    db_user = (
        db.query(models.UserDB)
        .filter(models.UserDB.login == pd_user.login)
        .first()
    )
    if not db_user:
        return {"status": False}
    elif db_user.password == pd_user.password:
        return {"status": True}
    else:
        return {"status": False}


@router.post("/reg")
def read_item(pd_user: schemas.UserPD, db: Session = Depends(get_db)):
    db_user = (
        db.query(models.UserDB)
        .filter(models.UserDB.login == pd_user.login)
        .first()
    )
    if not db_user:
        db_user = models.UserDB(
            login=pd_user.login,
            db_login=pd_user.login,
            password=pd_user.password,
            db_password=pd_user.password,
        )
        db.execute(
            text(
                f"CREATE SCHEMA IF NOT EXISTS {db_user.login} AUTHORIZATION root"
            )
        )
        db.add(db_user)
        db.commit()
        return {"status": True}
    return {"status": False}
