import base64
from fastapi import APIRouter, Depends, Request
from app.dto.teacher_dto import TeacherDTO, TeacherResponseDTO
from app.service.teacher_service import TeacherService
from app.models import teacher_model
from app.config.logger_config import get_logger
from app.utils.response_util import get_response

logger = get_logger()

teacher_route = APIRouter()

@teacher_route.get("/teacher")
async def get_all_teachers():
    logger.info(f"ENDPOINT CALLED: /TEACHER/(GET)\n DATA RECEIVED")
    
    # Fetch all teachers
    teachers = await TeacherService.get_all_teachers()

    # Fetch profile pictures for these teachers (assuming it returns a list of dicts)
    profile_pictures = await TeacherService.download_profile_pictures(teachers)
    print(profile_pictures)

    response = []

    # Iterate over each teacher
    for teacher in teachers:
        teacher_data = teacher.dict()  # Convert Pydantic model to dictionary

        # Check if the teacher has a profile_picture field
        if teacher.profile_picture:
            # Extract the profile picture file name
            profile_picture_filename = teacher.profile_picture
            
            # Find the profile picture content from the profile_pictures list
            profile_picture_content = next(
                (pic[profile_picture_filename] for pic in profile_pictures if profile_picture_filename in pic), None
            )

            # If the profile picture content is found, encode it as Base64 and add it to the teacher data
            if profile_picture_content:
                teacher_data['profile_picture_content'] = base64.b64encode(profile_picture_content).decode('utf-8')

        # Append the teacher data to the response list
        response.append(teacher_data)

    logger.info(f"RESPONSE SENT SUCCESSFULLY")
    return response


@teacher_route.get("/teacher/{teacher_id}")
async def get_teacher_by_id(teacher_id: str):
    logger.info(f"ENDPOINT CALLED:/TEACHER/(GET)\n DATA RECIEVED")
    response = await TeacherService.get_teacher_by_id(teacher_id)
    logger.info(f"RESPONSE SENT:{response}")
    return get_response(status="success",status_code=200,data=response)

@teacher_route.post("/teacher")
async def create_teacher(teacher: TeacherDTO = Depends(TeacherDTO.as_form)):
    logger.info(f"ENDPOINT CALLED:/TEACHER/(POST)\n DATA RECEIVED")
    response = await TeacherService.create_teacher(teacher)
    logger.info(F"RESPONSE SENT:RETRIEVED{response}")
    return get_response(status="success",status_code=200,message=response)

@teacher_route.get("/teacher/classes/{teacher_id}")
async def get_numOfClasses_students(teacher_id: str):
    logger.info(f"ENDPOINT CALLED:/TEACHER/CLASSES/(GET)\n DATA RECIEVED")
    response = await TeacherService.get_numOfClasses_students(teacher_id)
    logger.info(f"RESPONSE SENT:{response}")
    return get_response(status="success",status_code=200,data=response)
        

@teacher_route.delete("/teacher/{teacher_id}")
async def del_teacher(teacher_id: str):
    logger.info(f"ENDPOINT CALLED:/TEACHER/(DELETE)\n DATA RECEIVED")
    response = await TeacherService.delete_teacher(teacher_id)
    logger.info(F"RESPONSE SENT:RETRIEVED{response}")
    return get_response(status="success",status_code=200,message=response)
    
@teacher_route.put("/teacher/{teacher_id}")
async def update_teacher(teacher_id: str,teacher_dto:dict):
    logger.info(f"ENDPOINT CALLED:/TEACHER/(UPDATE)\n")
    response = await TeacherService.update_teacher(teacher_id,teacher_dto)
    logger.info(F"RESPONSE SENT:RETRIEVED{response}")
    return get_response(status="success",status_code=200,message=response)
