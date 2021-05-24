from fastapi import FastAPI,Depends,status,Response,HTTPException,APIRouter, Request
import hashing
from schemas import *
import models
from database import engine,SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import List,Tuple, Optional, Any
from hashing import Hash
from routers import jinja_test
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from itsdangerous import URLSafeTimedSerializer
from fastapi_sessions.backends import InMemoryBackend
from fastapi_sessions import SessionCookie, SessionInfo

#สร้าง FastAPI
app = FastAPI()

#สร้าง JinjaTemplate  เพื่อสร้างหน้า web ใช้ควบคู่กับ Fastapi
templates = Jinja2Templates(directory="templates")

#ทำการเชื่อมต่อ metadata
models.Base.metadata.create_all(engine)

#เรียกใช้ style.css ที่ถูกเก็บอยู่ใน Directory ชื่อ static
app.mount("/static", StaticFiles(directory="static"), name="static")

#Run router
app.include_router(jinja_test.router)


