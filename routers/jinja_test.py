from fastapi import Request,APIRouter,Form,Response,Depends,HTTPException,status
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_sessions.backends import InMemoryBackend
from fastapi_sessions import SessionCookie, SessionInfo
from typing import Tuple,Optional,List
from jose import JWTError, jwt

import models

from sqlalchemy.orm import Session

from database import *
from models import SessionData
from hashing import Hash
from token_2 import *

from datetime import datetime, timedelta

date = datetime.now()

#Create Session cookie
test_session = SessionCookie(
    name="session",
    secret_key="samplesession",
    backend=InMemoryBackend(),
    data_model=SessionData,
    scheme_name="TestSession",
    auto_error=False)

#Create router โดยตั้งชื่อ
router = APIRouter(prefix="/website")

templates = Jinja2Templates(directory="templates")

#Setting HTML
login_html = """
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Page</title>

        <!--<link href="{{ url_for('static', path='/styles.css') }}" rel="stylesheet"> -->
    </head>
    <body>
        <div class="header">
            <h2>Login</h2>
        </div>

        <form action="/website/auth" method="post">
            <!-- username //-->
            <div class="input-group">
                <label for="username">Username</label>
                <input type="text" name="username">
            </div>

            <!-- password //-->
             <div class="input-group">
                <label for="password">Password</label>
                <input type="password" name="password">
            </div>

            <div class="input-group">
                <button type="Submit" name="login_user" class="btn">Login</button>
            </div>
            <p>Forgot Password?<a href="updatepassword"> Forgot Password</a></p>
            <p>Not yet a member? <a href="register">Sign Up</a></p>
        </form>
    </body>
    </html>
        """

### Register ###
#1. หน้า Register Template
@router.get("/register", response_class=HTMLResponse,tags=['Register System'])
async def read_item(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

#1.1 สำหรับกรอกข้อมูลลง Database
@router.post("/register_db", response_class=HTMLResponse,tags=['Register System'])
def form_post(request: Request,db: Session = Depends(get_db),
              # Form(...) คือการรับค่าจาก register.html
              username: str = Form(...),
              email: str = Form(...),
              password_1: str = Form(...),
              password_2: str = Form(...)):

    #1.เช็ค Password ก่อนว่าเหมือนกันไหม (ทำก่อนเพราะไม่ต้องเชื่อม DB)
    if password_1 != password_2:
        return templates.TemplateResponse("register.html", {"request": request,
                                                            "error_message": "Password is not match.Please try again."})
    #2.Hash password เพราะจะไม่เก็บ Password ตรงๆลง DB
    password = Hash.becrypt(password_1)

    #3.เช็ค Username ก่อนว่ามีใน DB ยัง ถ้าไม่เท่ากับ None แปลว่ามี Username ดังกล่าวใน DB ให้ Return Error message ออกไป
    check_username = db.query(models.Register_db).filter(models.Register_db.username == username).first() #ค่าที่ออกมาเป็น Object
    if check_username != None:
        return templates.TemplateResponse("register.html", {"request": request,
                                                           "error_message": "Already username.Please try again."})

    #3.เช็ค Email ก่อนว่ามีใน DB ยัง ถ้าไม่เท่ากับ None แปลว่ามี Email ดังกล่าวใน DB ให้ Return Error message ออกไป
    check_email = db.query(models.Register_db).filter(models.Register_db.email == email).first() #ค่าที่ออกมาเป็น Object
    if check_email != None:
        return templates.TemplateResponse("register.html",{"request": request,
                                                           "error_message": "Already Email.Please try again."})

    #4.สร้าง Instance จาก Class Register_db ที่ชื่อ new_register_user ค่าที่ออกมาเป็น Object
    new_register_user = models.Register_db(username=username,
                                           email=email,
                                           password=password)

    #5.Add Instance ลง DB โดยใช้ Function.add
    db.add(new_register_user)
    db.commit()
    db.refresh(new_register_user) #หลัง Refress จะมี ID ขึ้นมาให้
    return templates.TemplateResponse("register.html",
                                      {"request": request,
                                       "error_message": "Register success.Please go to Sign in."})

#2. หน้า Login Template
@router.get("/login" ,response_class=HTMLResponse,tags=['Login System'])
async def read_item(request: Request, response: Response,db: Session = Depends(get_db)):
    html = login_html
    return html

#2.1 หน้า Auth username and password
@router.post("/auth",response_class=HTMLResponse,tags=['Login System'])
async def form_post(request: Request,
              response: Response,
              session_data: Optional[SessionInfo]=Depends(test_session),
              db: Session = Depends(get_db),
              username: str = Form(...),
              password: str = Form(...)):

    #สร้าง Object ขึ้นมาตัวนึงเอาไว้เป็นตัวเช็คข้อมูล
    check_username = db.query(models.Register_db).filter(models.Register_db.username == username).first()

    #สร้างตัว encode และ decode ตัว JWT ขึ้นมาเพื่อเอาไปใส่ใน cookie value
    encoded_jwt = create_access_token({
                                #"id": check_username.id,
                                "username": username,
                                "date": str(date)
                                       })

    decode_jwt = verify_token(encoded_jwt) #ค่าเป็น Dict
    # 2.1.1 เช็ค Username ก่อนว่ามีใน DB ยัง ถ้าเท่ากับ None แปลว่าไม่มี Username ดังกล่าวใน DB ให้ Return Error message ออกไป
    if check_username == None:
        return templates.TemplateResponse("index.html",
                                          {"request": request,
                                           "error_message": "Wrong username.Please try again."})
    #2.1.2 เช็ค Password โดยใช้ Function verify (hashing.py) โดยจะ Return เป็น Boolean ถ้าเป็น False แปลว่า Password ผิด
    if Hash.verify(check_username.password,password) == False:
        return templates.TemplateResponse("index.html",
                                          {"request": request,
                                           "error_message": "Wrong password.Please try again."})

    # 2.1.3 Create user_session โดยให้เก็บเป็น username อย่างเดียวเพราะมันเป็น Unique Value อยู่แล้ว(อยากเพิ่มตัวอื่นก็ไปเก็บใน schemas เพิ่ม)
    user_session = SessionData(session_data=encoded_jwt)
    await test_session.create_session(user_session, response)

    # 2.1.4 Setting cookie ในกรณีนี้ใส่ค่า name (เผื่อยัด jwt ลงไป)
    response.set_cookie("session",encoded_jwt,max_age=60)
    return "Login success"

#2.2 สร้างหน้าเว็ปสำหรับเข้า ตั้งชื่อว่า profile ซึ่งต้อง login ถึงจะเข้าได้เท่านั้น
@router.get("/profile" ,response_class=HTMLResponse,tags=['Login System'])
async def read_item(request: Request, response: Response):
    if request.cookies.get('session') == None: #request.cookies.get คือ value ของตัว cookies ส่วน 'session' คือชื่อของ session ในบรรทัดที่ 23
        return templates.TemplateResponse("index.html",
                                          {"request": request, "error_message": "Please Login again."})
    else:
        return templates.TemplateResponse("profile.html", {"request": request})

#2.3 หน้า Logout ต้องลบ Session และ cookie
@router.get("/logout",tags=['Login System'])
async def logout(request:Request,
                 response: Response,
                 session_data: Optional[SessionInfo]=Depends(test_session)):
    response.delete_cookie('session')
    return "Logout success"

#3. สร้างหน้าเว้ปสำหรับ Update password
@router.get("/updatepassword", response_class=HTMLResponse,tags=['Update Password System'])
async def read_item(request: Request):
    return templates.TemplateResponse("change_password.html", {"request": request})

#3.1 ทำการ Update password
@router.post("/update", response_class=HTMLResponse,tags=['Update Password System'])
def update_password(request: Request,db: Session = Depends(get_db),
              #เก็บข้อมูลจาก form ในหน้า updatepassword
              Username: str = Form(...),
              NewPassword: str = Form(...),
              ConfirmNewPassword: str = Form(...)):

    #3.1.1.เช็ค Password ก่อนว่าเหมือนกันไหม (ทำก่อนเพราะไม่ต้องเชื่อม DB)
    if NewPassword != ConfirmNewPassword:
        return templates.TemplateResponse("change_password.html",
                                          {"request": request,
                                           "message": "Password not match.Please try again."})

    #3.1.2.Hash password เพราะจะไม่เก็บ Password ตรงๆลง DB
    password = Hash.becrypt(NewPassword)

    #3.1.3.เช็ค Username ว่ามีใน DB ไหม (เช็คจาก register_db) ถ้าไม่มีก็แปลว่าไม่มี Username ดังกล่าว
    username = db.query(models.Register_db).filter(models.Register_db.username == Username)
    print("Username")#ค่าที่ออกมาเป็น Object
    print(username)

    if username.first() == None:
        return templates.TemplateResponse("change_password.html",
                                          {"request": request,
                                           "message": "Username : " + Username + " not found. Please try again."})

    #3.1.4. เริ่มทำการ Update password และ commit db
    username.update({'password':password})
    db.commit()

    # 3.1.5 Return ข้อความว่า Update Success
    return templates.TemplateResponse("change_password.html",
                                      {"request": request,
                                       "message": "Username : " + Username + " update complete. Please go to Sign in."})