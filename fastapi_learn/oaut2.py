from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from token_2 import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def get_current_user(token:str=Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token,credentials_exception)



