from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#สร้างตัวแปร DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

#สร้างตัวเชื่อมต่อกับฐานข้อมูล sqlite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

#สร้าง sessionlocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#สร้างแบบจำลอง Base
Base = declarative_base()

#Create Function ชื่อ get_db เพื่อเชื่อม DB (ใช้ yield เป็นตัว generator และ close มัน)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()