
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