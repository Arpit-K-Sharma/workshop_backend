import random
from fastapi import HTTPException
from app.repositories.school_repo import SchoolRepository
from app.repositories.student_repo import StudentRepository
from app.models.student_model import Student
from app.dto.student_dto import StudentDTO,StudentResponseDTO


class StudentService: 
    @staticmethod
    async def generate_unique_email(student_name: str, school_id: str):
        from app.service.school_service import SchoolService
        # Get the school
        school = await SchoolRepository.get_school(school_id)
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        
        # Split the student name
        name_parts = student_name.split()
        first_name = name_parts[0].lower()
        
        # Generate the name part of the email
        if len(name_parts) > 1:
            # If there are additional names, add their first characters before the first name
            additional_initials = ''.join(name.lower()[0] for name in name_parts[1:])
            name_for_email = f"{additional_initials}{first_name}"
        else:
            name_for_email = first_name
        
        # Abbreviate the school name
        school_abbr = SchoolService.abbreviate_school_name(school['school_name']).lower()
        
        # Create the base email
        base_email = f"{name_for_email}@{school_abbr}.edu.np"
        
        # Check if the email already exists
        existing_student = await StudentRepository.get_student_by_email(base_email)
        
        if not existing_student:
            return base_email, school['school_code']
        
        # If email exists, add random numbers
        attempt = 0
        while True:
            attempt += 1
            random_numbers = ''.join([str(random.randint(0, 9)) for _ in range(2)])
            new_email = f"{name_for_email}{random_numbers}@{school_abbr}.edu.np"
            existing_student = await StudentRepository.get_student_by_email(new_email)
            if not existing_student:
                return new_email, school['school_code']
            if attempt > 99:  # Avoid infinite loop
                raise HTTPException(status_code=500, detail="Unable to generate a unique email after multiple attempts")

    @staticmethod
    async def create_student(studentdto: StudentDTO):
        try:
            # Generate unique email and get school_code
            unique_email, school_code = await StudentService.generate_unique_email(
                studentdto.student_name, 
                studentdto.school_id
            )

            
            # Add the generated email and school_code (as password) to the student data
            student = Student(**studentdto.dict(exclude_unset=True))
            student_data = student.dict()
            student_data['student_email'] = unique_email
            student_data['password'] = school_code
            
            result = await StudentRepository.create_student(student_data)
            if result:
                return "Student Created Successfully"
            raise HTTPException(status_code=400, detail="Could not create student")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while creating the student: {str(e)}")
    
    @staticmethod
    async def get_student_by_id(student_id: str):
        try:
            result = await StudentRepository.get_student_by_id(student_id)
            return StudentResponseDTO(**result)
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"An error occurred while fetching the student: {str(e)}")
        
    @staticmethod
    async def get_students_by_school_id(school_id: str):
        try:
            result = await StudentRepository. get_students_by_school_id(school_id)
            return [StudentResponseDTO(**school) async for school in result]
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"An error occurred while fetching the School: {str(e)}")
    

    @staticmethod
    async def get_all_students():
        try:
            result = await StudentRepository.get_all_student()
            return [StudentResponseDTO(**student) async for student in result]
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"An error occurred while fetching all students: {str(e)}")
    
    @staticmethod
    async def delete_student(student_id: str):
        try:
            result = await StudentRepository.delete_student(student_id)
            return {"message": result}
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"An error occurred while deleting the student: {str(e)}")

    @staticmethod
    async def update_student(student_id: str, student: StudentDTO):
        try:
            result = await StudentRepository.update_student(student_id, student)
            if isinstance(result, str):
                # If result is a string, it's a message from the repository
                return result
            else:
                # If result is not a string, it should be an UpdateResult object
                if result.matched_count == 0:
                    raise HTTPException(status_code=404, detail="Student not found")
                
                if result.modified_count > 0:
                    return "Student updated successfully"
                else:
                    return "No changes made to the student"
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"An error occurred while updating the student: {str(e)}")
        
    @staticmethod
    async def get_student_by_email(email: str):
        try:
            result = await StudentRepository.get_student_by_email(email)
            if result:
                return StudentResponseDTO(**result)
            raise HTTPException(status_code=404, detail="Student not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching the student: {str(e)}")
        
        