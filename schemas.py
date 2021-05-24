from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

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

class Registerdb(BaseModel):
    username:str
    email:str
    password_1:str





