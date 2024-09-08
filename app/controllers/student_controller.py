import base64
from fastapi import APIRouter, Depends, Request
from app.dto.student_dto import StudentDTO
from app.service.student_service import StudentService
from app.models.student_model import Student
from app.config.logger_config import get_logger
from app.utils.response_util import get_response

logger = get_logger()

student_route = APIRouter()

@student_route.get("/student/{student_id}")
async def get_student_by_id(student_id: str):
    logger.info(f"ENDPOINT CALLED:/STUDENT/(GET)\n DATA DELETED")
    response = await StudentService.get_student_by_id(student_id)
    logger.info(f"RESPONSE SENT:{response}")
    return get_response(status="success",status_code=200,data=response)

@student_route.get("/student/school/{school_id}")
async def get_students_by_school_id(school_id: str):
    logger.info(f"ENDPOINT CALLED:/STUDENT/(GET)\n DATA TAKEN")
    response = await StudentService.get_students_by_school_id(school_id)
    logger.info(f"RESPONSE SENT:{response}")
    return get_response(status="success",status_code=200,data=response)


@student_route.get("/student")
async def get_all_students():
    logger.info(f"ENDPOINT CALLED: /STUDENT/(GET)\n DATA TAKEN")

    # Fetch all students
    students = await StudentService.get_all_students()
    
    # Fetch profile pictures for these students (assuming it returns a list of dicts)
    profile_pictures = await StudentService.download_profile_pictures(students)

    response = []
    
    # Iterate over each student
    for student in students:
        student_data = student.dict()  # Convert Pydantic model to dictionary

        # Check if the student has a profile_picture field
        if student.profile_picture:
            # Extract the profile picture file name
            profile_picture_filename = student.profile_picture
            
            # Find the profile picture content from the profile_pictures list
            profile_picture_content = next(
                (pic[profile_picture_filename] for pic in profile_pictures if profile_picture_filename in pic), None
            )

            # If the profile picture content is found, encode it as Base64 and add it to the student data
            if profile_picture_content:
                student_data['profile_picture_content'] = base64.b64encode(profile_picture_content).decode('utf-8')

        # Append the student data to the response list
        response.append(student_data)

    logger.info(f"RESPONSE SENT SUCCESSFULLY")
    return response

@student_route.post("/student")
async def create_student(student: StudentDTO = Depends(StudentDTO.as_form)):
    logger.info(f"ENDPOINT CALLED:/STUDENT/(POST)\n DATA RECEIVED")
    response = await StudentService.create_student(student)
    logger.info(f"RESPONSE SENT:{response}")
    return get_response(status="success",status_code=200,message=response)

@student_route.delete("/student/{student_id}")
async def delete_Student(student_id: str):
    logger.info(f"ENDPOINT CALLED:/STUDENT/(DELETE)\n DATA DELETED")
    response = await StudentService.delete_student(student_id)
    logger.info(f"RESPONSE SENT:{response}")
    return get_response(status="success",status_code=200,message=response)

@student_route.put("/student/{student_id}")
async def update_Student(student_id: str, student: dict):
    logger.info(f"ENDPOINT CALLED:/STUDENT/(UPDATE)\n DATA UPDATED")
    response = await StudentService.update_student(student_id, student)
    logger.info(f"RESPONSE SENT:{response}")
    return get_response(status="success",status_code=200,message=response)


@student_route.get("/student/email/{email}")
async def get_student_by_email(email: str):
    logger.info(f"ENDPOINT CALLED:/STUDENT/EMAIL/(GET)\n DATA TAKEN")
    response =  await StudentService.get_student_by_email(email)
    logger.info(f"RESPONSE SENT:{response}")
    return get_response(status="success",status_code=200,data=response)

@student_route.put("/student/changePassword/{student_id}")
async def change_password(student_id:str, new_password: str):
    logger.info(f"ENDPOINT CALLED:/STUDENT/CHANGEPASSWORD/{student_id}(PUT)\n DATA TAKEN")
    response = await StudentService.change_password(student_id,new_password)
    logger.info(f"PASSWORD CHANGED SUCCESSFULLY FOR {student_id}")
    return get_response(status="success",status_code=200,message=response)


