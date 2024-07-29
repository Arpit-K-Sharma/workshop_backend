from fastapi import APIRouter
from app.models.teacher_model import Teacher
from app.service.teacher_service import TeacherService

teacher_route = APIRouter()

@teacher_route.get("/teacher")
async def list_teachers(teacher:Teacher):
    response = await TeacherService.list_teacher(teacher)
    return response

@teacher_route.get("/teacher/{teacher_id}")
async def read_teacher(teacher_id:str):
    response =await TeacherService.read_teacher(teacher_id)  
    return response
    
@teacher_route.post("/teacher")
async def post_teacher(teacher:Teacher):
    response =await TeacherService.create_teacher(teacher)
    return response
    
@teacher_route.delete("/teacher/{teacher_id}")
async def del_teacher(teacher_id:str):
    response = await TeacherService.delete_teacher(teacher_id)
    return response

@teacher_route.put("/teacher/{teacher_id}")
async def put_teacher(teacher_id:str, teacher:Teacher):
    response = await TeacherService.update_teacher(teacher_id, teacher)
    return response