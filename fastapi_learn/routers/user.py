from fastapi import APIRouter, Depends,status,Response,HTTPException
from typing import List
import schemas
import models
from database import *
from sqlalchemy.orm import Session
import hashing
from hashing import Hash
from repository import user, log
from jose import JWTError, jwt
from oaut2 import *

router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.post('/', response_model=schemas.User)
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    # new_user = models.User(name = request.name,
    #                        email = request.email,
    #                        #password = request.password))
    #                        password = Hash.becrypt(request.password))
    # #new_user = models.User(request) #requests ใช้ไม่ได้ เขียนไว้สำรอง
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    # return new_user
    return user.create(request, db)

@router.get('/', response_model=List[schemas.ShowUser])
def all_user(db: Session = Depends(get_db)):
    # user = db.query(models.User).all()
    # return user
    return user.get_all(db)

@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id,response : Response, db:Session = Depends(get_db)):
    # user = db.query(models.User).filter(models.User.id == id).first()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail = f"User with id {id} is not available!.")
    # return user
    return user.show(id,db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(id, request: schemas.User, db: Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    # user = db.query(models.User).filter(models.User.id == id)
    # if not user.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"User with id {id} is not found!")
    # user.update({'name':request.name,
    #              'email':request.email,
    #              'password':request.password})
    # db.commit()
    # return f'Update user id{id} done'
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # username: str = payload.get("sub")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #write ลง database
    log.create(payload["username"],"Updated!",id,db)
    return user.update(id,request,db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db:Session = Depends(get_db)):
    # user=db.query(models.User).filter(models.User.id == id)
    # if not user.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"User with id {id} is not found!")
    # user.delete(synchronize_session=False)
    # db.commit() #Confirm
    # return f'Delete User id {id} done'
    # return user.update(id,request,db)
    return user.delete(id,db)


