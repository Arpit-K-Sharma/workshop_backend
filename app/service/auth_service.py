from fastapi import HTTPException
from app.config.db_config import mongodb
from app.utils.auth_utils import create_access_token
from app.utils.password_utils import verify_password

class AuthService:
    async def admin_login(email: str, password: str):
        admin = await mongodb.collections['admin'].find_one({"role": "ADMIN"})
        
        if admin is None:
            raise HTTPException(status_code=400, detail="Admin not found")
        
        # Check if 'email' and 'password' keys exist in the admin object
        if 'email' not in admin or 'password' not in admin:
            raise HTTPException(status_code=400, detail="Invalid admin data")
        
        if email == admin['email'] and verify_password(password,admin['password']):
            access_token = create_access_token(data={"email": email, "role": "ADMIN"})
            return {"access_token": access_token, "token_type": "bearer"}
        
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    async def mentor_login(email:str, password:str):
        mentor = await mongodb.collections['teacher'].find_one({"username":email})
        id = str(mentor['_id'])
        if mentor and email == mentor['username'] and verify_password(password,mentor['password']):
            access_token = create_access_token(data={"email":email,"id":id,"role":"MENTOR"})
            return {"access_token":access_token, "token_type": "bearer"}
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    
    async def student_login(email:str, password:str):
        student = await mongodb.collections['student'].find_one({"studentId":email})
        id = str(student['_id'])
        if student and email == student['studentId'] and verify_password(password,student['password']):
            access_token = create_access_token(data={"email":email,"id":id, "role":"STUDENT"})
            return {"access_token":access_token, "token_type": "bearer"}
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    async def school_login(email:str, password:str):
        school = await mongodb.collections['school'].find_one({"email":email})
        id = str(school['_id'])
        if school and email == school['email'] and verify_password(password,school['password']):
            access_token = create_access_token(data={"email":email,"id":id, "role":"SCHOOL"})
            return {"access_token":access_token, "token_type": "bearer"}
        raise HTTPException(status_code=400, detail="Invalid credentials")