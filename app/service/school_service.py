import random
from fastapi import HTTPException
from app.repositories.school_repo import SchoolRepository
from app.models.school_model import School
from app.dto.school_dto import SchoolDTO, SchoolResponseDTO
from app.service.course_service import CourseService
from app.service.student_service import StudentService

class SchoolService:
    @staticmethod
    async def create_school(schooldto: SchoolDTO):
        # Convert SchoolDTO to School object
        school = School(**schooldto.dict())

        # # Upload banner file
        # if banner is not None:
        #     banner_result = await FileService.upload_file(banner)
        #     school.banner = banner_result["file_id"]
        
        # # Upload logo file
        # if logo is not None:
        #     logo_result = await FileService.upload_file(logo)
        #     school.logo = logo_result["file_id"]

        school_name_abbr = SchoolService.abbreviate_school_name(school.school_name)
        random_numbers = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        school_code = f"{school_name_abbr}{random_numbers}"

        # Add school code to the school object
        school.school_code = school_code
        
        # Create school
        result = await SchoolRepository.create_school(school)
        if result:
            return "School created successfully"
        raise HTTPException(status_code=400, detail="School not created")

    
    @staticmethod
    async def get_all_school():
        results = await SchoolRepository.get_all_schools()  # Update method name here
        return [SchoolResponseDTO(**school) for school in results]

    @staticmethod
    async def get_school(school_id: str) -> SchoolResponseDTO:
        result = await SchoolRepository.get_school(school_id)
        if isinstance(result, dict):
            return SchoolResponseDTO(**result)
        raise HTTPException(status_code=404, detail="School not found")

    @staticmethod
    async def delete_school(school_id: str):
        result = await SchoolRepository.delete_school(school_id)
        if result == "School deleted successfully":
            return result
        raise HTTPException(status_code=404, detail=f"School with id {school_id} not found")

    @staticmethod
    async def update_school(school_id: str, schooldto: SchoolDTO):
        # First, get the existing school data
        existing_school = await SchoolRepository.get_school(school_id)
        if not existing_school:
            raise HTTPException(status_code=404, detail=f"School with id {school_id} not found")


        # Create a dict of the new data, excluding None values
        update_data = {k: v for k, v in schooldto.dict(exclude_unset=True).items() if v is not None}
        print(update_data)

        updated_school = School(**update_data)
        result = await SchoolRepository.update_school(school_id, updated_school)

        if result == "School updated successfully":
            return result
        raise HTTPException(status_code=500, detail="Failed to update school")

    
    
    @staticmethod
    def abbreviate_school_name(name):
        words = name.split()
        if len(words) > 1:
            return ''.join(word[0].upper() for word in words)
        return name


    @staticmethod
    async def get_students_per_course():
        schoolResponse = await SchoolService.get_all_school()
        courseResponse = await CourseService.get_all_courses()
        studentResponse = await StudentService.get_all_students()

        course_per_school_dict = [
            {
                "schoolId": school.id,
                "schoolName": SchoolService.abbreviate_school_name(school.school_name),
                **{course.course_name: 0 for course in courseResponse}
            }
            for school in schoolResponse
        ]

        for school in schoolResponse:
            for student in studentResponse:
                if student.school_id == school.id:
                    for course_id in student.course_id:
                        for course in courseResponse:
                            if course.id == course_id:
                                for entry in course_per_school_dict:
                                    if entry["schoolId"] == school.id:
                                        entry[course.course_name] += 1

        # for student in studentResponse:
        #     for course_id in student.course_id:
        #         for course in courseResponse:
        #             if course.id == course_id:
        #                 school_entry = next(
        #                         entry for entry in course_per_school_dict
        #                         if entry["school_name"] == next(school.school_name for school in schoolResponse if school.id == student.school_id)
        #                         )
        #                 school_entry[course.course_name] += 1

        # Remove schoolId from each entry before returning
        for entry in course_per_school_dict:
            del entry["schoolId"]

        return course_per_school_dict
    

    



