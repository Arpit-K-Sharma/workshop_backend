from fastapi import APIRouter
from app.models.auth_model import AuthModel
from app.service.auth_service import AuthService


auth_route = APIRouter()

@auth_route.post("/admin/login")
async def admin_login(admin_auth: AuthModel):
    return await AuthService.admin_login(admin_auth.username, admin_auth.password)