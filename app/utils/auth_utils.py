from datetime import datetime, timedelta
import os
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    

async def admin_verification(token:str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not is_admin(payload):
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return payload

def is_admin(payload: dict) -> bool:
    role = payload.get("role")
    if (role == "ADMIN"):
        return True
    else:
        return False
    

async def mentor_verification(token:str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not is_mentor(payload):
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return payload


def is_mentor(payload):
    role = payload.get("role")
    if(role == "MENTOR"):
        return True
    else:
        return False
    

async def student_verification(token:str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not is_student(payload):
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return payload


def is_student(payload):
    role = payload.get("role")
    if(role == "STUDENT"):
        return True
    else:
        return False

