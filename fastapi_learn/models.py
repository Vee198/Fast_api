from database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey,DateTime
from sqlalchemy.orm import relationship


#Define every filed in database and connect table
class Blog(Base): #Base is refer database from database.py
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index = True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id')) #สำหรับเป็น Foreignkey ในการเชื่อมกับ user table

    creator = relationship("User", back_populates="blogs") #Create Relationshio

 #-------------------------- User Session --------------------------
class User(Base): #Base is refer database from database.py
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("Blog", back_populates="creator") #Create Relationshion

class Log(Base): #Base is refer database from database.py
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String)
    time = Column(DateTime)
    action = Column(String)
    detail = Column(String)


