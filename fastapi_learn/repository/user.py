from sqlalchemy.orm import Session
import models
import schemas
from fastapi import HTTPException,status
import hashing
from hashing import Hash

def get_all(db:Session):
    user = db.query(models.User).all()
    return user

def create(request:schemas.Blog,db:Session):
    new_user = models.User(name = request.name,
                           email = request.email,
                           password = Hash.becrypt(request.password))
    #new_user = models.User(request) #requests ใช้ไม่ได้ เขียนไว้สำรอง
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id:int,db:Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} is not avaiable!")
    return user

def update(id:int, request:schemas.Blog,db:Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} is not found!")
    user.update({'name': request.name,
                 'email': request.email,
                 'password':request.password})
    db.commit()
    return f'update blog id{id} done.'

def delete(id:int, db:Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} is not found!")
    user.delete(synchronize_session=False)
    db.commit()  # Confirm
    return f'Delete User id {id} done'
    return user.update(id, request, db)



