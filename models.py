from database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel

#กำหนด Model ที่ชื่อ Register_db โดยข้อมูลต้องอ้างอิงจาก database.py และ DB (ตัว Base)
class Register_db(Base):
    __tablename__ = 'registerdb'
    id = Column(Integer, primary_key=True, index = True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

#ข้อมูลสำหรับการเก็บ website session
class SessionData(BaseModel):
    session_data:str


