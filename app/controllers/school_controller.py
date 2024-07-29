from fastapi import APIRouter
from app.models.school_model import School
from app.service.school_service import schoolService

school_route = APIRouter()

@school_route.get("/school")
async def list_schools(school:School):
    response = await schoolService.list_school(school)
    return response

@school_route.get("/school/{school_id}")
async def read_school(school_id:str):
    response =await schoolService.read_school(school_id)  
    return response
    
@school_route.post("/school")
async def post_school(school:School):
    response =await schoolService.create_school(school)
    return response
    
@school_route.delete("/school/{school_id}")
async def del_school(school_id:str):
    response = await schoolService.delete_school(school_id)
    return response

@school_route.put("/school/{school_id}")
async def put_school(school_id:str, school:School):
    response = await schoolService.update_school(school_id, school)
    return response