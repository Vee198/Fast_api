from fastapi import APIRouter, Depends,status,Response,HTTPException
from typing import List
from database import *
from sqlalchemy.orm import Session
from repository import blog, log
from oaut2 import *
from datetime import datetime
import oaut2
import models
from schemas import *
from jose import JWTError, jwt
from oaut2 import *

date = datetime.now()
day = date.strftime('%c')

router = APIRouter(
    prefix="/blog",
    tags=['Blog']
)

@router.post('/',status_code=status.HTTP_201_CREATED) #Status code is 201 status(Create success)
#def create(request: schemas.Blog, db: Session = Depends(get_db),get_current_user:schemas.User=Depends(oaut2.get_current_user)):
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    # new_blog = models.Blog(title=request.title,
    #                        body=request.body,
    #                        user_id=1)
    # db.add(new_blog)
    # db.commit() #Confirm
    # db.refresh(new_blog)
    # return new_blog
    return blog.create(request,db)

@router.get('/',response_model=List[schemas.Showblog])
#def all_blog(db: Session = Depends(get_db),get_current_user:schemas.User=Depends(oaut2.get_current_user)):
def all_blog(db: Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    # blogs = db.query(models.Blog).all()
    # return blogs
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # username: str = payload.get("sub")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # write ลง database
    log.create(payload["username"], "Get blog!", "Get all blog!", db)
    return blog.get_all(db)

@router.get('/{id}',status_code=200, response_model=schemas.Showblog) #Response model for don't show id
#def get_id(id:int,response : Response, db:Session = Depends(get_db),get_current_user:schemas.User=Depends(oaut2.get_current_user)):
def get_id(id:int,response : Response, db:Session = Depends(get_db)):
    #blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # if not blog:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Blog with id {id} is not avaiable!")
    # return blog
    #get token for tracking
    #email = db.query(models.User).filter(models.User.email == request.username).first()
    access_token = create_access_token(data={"id" : id,"time": day})
    #print(access_token)
    return blog.show(id,db)
    #return access_token
    #return {"access_token": access_token, "token_type": "bearer"}

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
#def update_blog(id:int, request: schemas.Blog, db: Session = Depends(get_db),get_current_user:schemas.User=Depends(oaut2.get_current_user)):
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id == id)
    # if not blog.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Blog with id {id} is not found!")
    # blog.update({'title': request.title, 'body': request.body})
    # db.commit()
    # return f'update blog id{id} done.'

    return blog.update(id,request,db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
#def destroy(id:int,db:Session = Depends(get_db),get_current_user:schemas.User=Depends(oaut2.get_current_user)):
def destroy(id:int,db:Session = Depends(get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id == id)
    # if not blog.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Blog with id {id} is not found!")
    # blog.delete(synchronize_session=False)
    # db.commit() #Confirm
    # return f'Delete blog id{id} done.'
    return blog.delete(id,db)