from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

date = datetime.now()

class Blog(BaseModel):
    title: str
    body: str
    #access_token :str
    class Config: #แปลง Object ให้ปเ็น Dict หรือ Json
        orm_mode = True

# -------------------------- User Session --------------------------
class User(BaseModel):
    name: str
    email: str
    password: str
    class Config: #แปลง Object ให้ปเ็น Dict หรือ Json
        orm_mode = True

class UserBase(User):  #ดึง all list in user database  ซึ่งมี ID รวมอยู่ด้วย
    class Config: #แปลง Object ให้ปเ็น Dict หรือ Json
        orm_mode = True

class ShowUser(UserBase):  #ดึง all list cloumn in user database
    name: str
    email: str
    #blogs: List[Blog]=[]
    password : str # Because don't show password of user
    class Config: #แปลง Object ให้ปเ็น Dict หรือ Json
        orm_mode = True
class Showblog(Blog):
    title: str
    body: str
    creator: ShowUser
    #access_token: str #สร้างมาเพื่อ track หน้า
    class Config(): #แปลง Object ให้ปเ็น Dict หรือ Json
        orm_mode = True

class Login(BaseModel):
    username:str
    #email:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None

class Log(BaseModel):
    user:str
    time:str
    action:str
    detail:int









