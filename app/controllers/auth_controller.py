from fastapi import APIRouter
from app.models.auth_model import AuthModel
from app.service.auth_service import AuthService



auth_route = APIRouter()


@auth_route.post("/admin/login")
async def admin_login(admin_auth: AuthModel):
    return await AuthService.admin_login(admin_auth.email, admin_auth.password)

@auth_route.post("/mentor/login")
async def mentor_login(mentor_auth: AuthModel):
    return await AuthService.mentor_login(mentor_auth.email, mentor_auth.password)

@auth_route.post("/student/login")
async def student_login(student_auth: AuthModel):
    return await AuthService.student_login(student_auth.email, student_auth.password)