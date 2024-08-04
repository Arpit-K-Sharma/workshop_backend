from fastapi import HTTPException
from app.repositories.course_repo import CourseRepository
from app.models.course_model import Course
from app.dto.course_dto import CourseDTO, CourseResponseDTO

class CourseService:
    @staticmethod
    async def create_course(coursedto: CourseDTO):
        course = Course(**coursedto.dict())
        result = await CourseRepository.create_course(course)
        if result:
            return "Course created successfully"
        return HTTPException(status_code=400, detail="Course is not created")

    @staticmethod
    async def get_all_courses():
        results = await CourseRepository.get_all_courses()  # Update method name here
        return [CourseResponseDTO(**course) if course else None for course in results]

    @staticmethod
    async def get_course(course_id: str):
        result = await CourseRepository.get_course(course_id)
        if not result:
            raise HTTPException(status_code=404, detail="No course found by course id")
        return result



    @staticmethod
    async def delete_course(course_id: str):
        result = await CourseRepository.delete_course(course_id)
        if result is None:
            raise HTTPException(
                status_code=400,
                detail=f"Course with id {course_id} not found"
            )
        return result

    @staticmethod
    async def update_course(course_id: str, coursedto: CourseDTO):
        course = Course(**coursedto.dict())
        result = await CourseRepository.update_course(course_id, course)
        if result is None:
            raise HTTPException(
                status_code=400,
                detail=f"Course with id {course_id} not found"
            )
        return result
