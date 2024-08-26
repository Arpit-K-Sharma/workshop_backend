from fastapi import HTTPException
from app.config.db_config import mongodb
from app.utils.auth_utils import create_access_token

class AuthService:
    async def admin_login(username: str, password: str):
        admin = await mongodb.collections['admin'].find_one({"role": "ADMIN"})
        
        # Debugging: Print the admin object
        print("Admin object:", admin)
        
        if admin is None:
            raise HTTPException(status_code=400, detail="Admin not found")
        
        # Check if 'email' and 'password' keys exist in the admin object
        if 'username' not in admin or 'password' not in admin:
            raise HTTPException(status_code=400, detail="Invalid admin data")
        
        if username == admin['username'] and password == admin['password']:
            access_token = create_access_token(data={"username": username, "role": "ADMIN"})
            return {"access_token": access_token, "token_type": "bearer"}
        
        raise HTTPException(status_code=400, detail="Invalid credentials")
