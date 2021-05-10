from sqlalchemy.orm import Session
import models
import schemas
from fastapi import HTTPException,status
import hashing
from hashing import Hash
from datetime import datetime

date = datetime.now()

def create(username:str,action:str,detail:str,db:Session):
    new_log = models.Log(name = username,
                           time = date,
                           action=action,
                           detail = detail)
    #new_user = models.User(request) #requests ใช้ไม่ได้ เขียนไว้สำรอง
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log