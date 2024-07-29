from fastapi import APIRouter
from app.models.student_model import Student
from app.service.student_service import studentService

student_route = APIRouter()

student_route.get("/student")
async def list_students(student:Student):
    response = await studentService.list_student(student)
    return response
@student_route.get("/student")
async def read_student():
    response =await studentService.read_student()  
    return response
    
@student_route.post("/student")
async def post_student(student:Student):
    response =await studentService.create_student(student)
    return response
    
@student_route.delete("/student/{student_id}")
async def del_student(student_id:str):
    response = await studentService.delete_student(student_id)
    return response
@student_route.put("/student/{student_id}")
async def put_student(student_id:str, student:Student):
    response = await studentService.update_student(student_id, student)
    return response