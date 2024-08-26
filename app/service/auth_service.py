
from fastapi import HTTPException
from app.config.db_config import mongodb
from app.utils.auth_utils import create_access_token


class AuthService:
    async def admin_login(email:str, password:str):
        admin = await mongodb.collections['admin'].find_one({"role":"ADMIN"})
        if admin and email == admin['email'] and password == admin['password']:
            access_token = create_access_token(data={"email":email, "role":"ADMIN"})
            return {"access_token":access_token, "token_type": "bearer"}
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    async def mentpr_login(email:str, password:str):
        mentor = await mongodb.collections['teacher'].find_one({"email":email})
        if mentor and email == mentor['email'] and password == mentor['password']:
            access_token = create_access_token(data={"email":email, "role":"MENTOR"})
            return {"access_token":access_token, "token_type": "bearer"}
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    async def student_login(email:str, password:str):
        student = await mongodb.collections['student'].find_one({"student_email":email})
        if student and email == student['email'] and password == student['password']:
            access_token = create_access_token(data={"email":email, "role":"STUDENT"})
            return {"access_token":access_token, "token_type": "bearer"}
        raise HTTPException(status_code=400, detail="Invalid credentials")