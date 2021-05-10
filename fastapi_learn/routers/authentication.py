#Import Library ที่ต้องใช้
from fastapi import FastAPI,Depends,status,Response,HTTPException,APIRouter
import schemas
from database import *
from sqlalchemy.orm import Session
import models
from hashing import Hash
from datetime import datetime, timedelta
from token_2 import *
from fastapi.security import OAuth2PasswordRequestForm
from oaut2 import *
from datetime import datetime

date = datetime.now()
day = date.strftime('%c')

#Create Router เป็นเหมือน Channel ให้เป็นระเบียบ จะได้ไม่ต้องไปกอง Code อยู่ที่ Main
router = APIRouter(
    tags=['Authentication'] #กำหนด tag name เพื่อบอกกลุ่มว่าเป็นกลุ่มที่ทำ Authentication
)

#สร้าง blog สำหรับ write ข้อมูล(Post) และตั้งชื่อ path ว่า login
@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session =Depends(get_db)): #ใช้สำหรับทำเป็นระบบที่ต้องกรอก ID และ Password ถึงจะทำงานไ้

    #1.1..สร้างตัวแปร user สำหรับไป Query ช่อง user ใน Database
    #user=db.query(models.User).filter(models.User.name == request.username).first()
    #1.2..สร้างตัวแปร email สำหรับไป Query ช่อง Email ใน Database
    email = db.query(models.User).filter(models.User.email == request.username).first()

    #2.1.ตรวจสอบเงื่อนไขกรณี User ที่กรอกมาไม่ตรง ให้ Return Status HTTP_404_NOT_FOUND และ ค่ากลับมาเป็น Invalid Credentials
    # if not user: #กรณีต้องการใช้ username ในการ login
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                 detail=f"Invalid Credentials")

    #2.2.ตรวจสอบเงื่อนไขกรณี Email ที่กรอกมาไม่ตรง ให้ Return Status HTTP_404_NOT_FOUND และ ค่ากลับมาเป็น Invalid Email
    if not email:  #กรณีต้องการใช้ email ในการ login
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Email")

    #3.ตรวจสอบเงื่อนไขกรณี Password ที่กรอกมาไม่ตรง ให้ Return Status HTTP_404_NOT_FOUND และ ค่ากลับมาเป็น Invalid Email
    #if not Hash.verify(user.password,request.password): #If want to user username for login
    if not Hash.verify(email.password, request.password): #If want to user email for login
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    #4.สร้าง Access token
    #access_token = create_access_token(data={"email": user.email, "username":user.username}) #กรณีต้องการใช้ username ในการ login
    access_token = create_access_token(data={"time":day,"email": email.email, "username":email.name}) #กรณีต้องการใช้ email ในการ login

    #6.ให้โปรแกรม Return ค่า access token ตามข้อ 5 ออกมา
    return {"access_token": access_token, "token_type": "bearer"}

#สร้าง blog สำหรับ Show ข้อมูล Current User ที่ Login เข้ามาล่าสุด และตั้งชื่อ path ว่า me
@router.get('/me')
async def get_current_user(token:str=Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # username: str = payload.get("sub")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return payload

#สร้าง blog สำหรับ write ข้อมูล(Post) และตั้งชื่อ path ว่า login
#@router.post('/logout')
#def logout(request:OAuth2PasswordRequestForm=Depends(),db:Session =Depends(get_db)): #ใช้สำหรับทำเป็นระบบที่ต้องกรอก ID และ Password ถึงจะทำงานไ้