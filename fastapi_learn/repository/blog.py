from sqlalchemy.orm import Session
import models
import schemas
from fastapi import HTTPException,status

def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request:schemas.Blog,db:Session):
    new_blog = models.Blog(title=request.title,
                           body=request.body,
                           user_id=1)
    db.add(new_blog)
    db.commit()  # Confirm
    db.refresh(new_blog)
    return new_blog

def delete(id:int, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} is not found!")
    blog.delete(synchronize_session=False)
    db.commit()  # Confirm
    return f'Delete blog id{id} done.'

def update(id:int, request:schemas.Blog,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} is not found!")
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return f'update blog id{id} done.'

def show(id:int,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} is not avaiable!")
    return blog