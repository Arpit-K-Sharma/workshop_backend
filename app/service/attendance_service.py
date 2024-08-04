from datetime import datetime
from typing import List, Optional
from bson import DBRef, ObjectId
from fastapi import HTTPException
from app.repositories.attendance_repo import AttendanceRepository
from app.models.attendance_model import Attendance
from app.dto.attendance_dto import AttendanceDTO, AttendanceResponseDTO, StudentStatusResponseDTO, TeacherStatusResponseDTO, SchoolStatusResponseDTO
from app.config.logger_config import get_logger

class AttendanceService:
    def __init__(self, repository: AttendanceRepository):
        self.attendance_repository = repository
        self.logger = get_logger()

    def validate_input(self, input_value):
        if input_value is None or input_value == "":
            return False
        return True

    async def create_attendance(self, attendance_dto: AttendanceDTO) -> str:
        if not self.validate_input(attendance_dto):
            raise HTTPException(status_code=400, detail="Invalid input for attendance_dto")
        self.logger.info("Creating attendance")
        try:
            attendance = Attendance(**attendance_dto.dict())
            return await self.attendance_repository.create_attendance(attendance)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating attendance: {str(e)}")


    async def get_all_attendances(self) -> List[AttendanceResponseDTO]:
        self.logger.info("Retrieving all attendances")
        try:
            attendances_cursor = await self.attendance_repository.get_all_attendances()
            print(attendances_cursor)
            attendances = []
            for attendance in attendances_cursor:
                school_attendances=[]
                for school in attendance.schools:
                    student_attendance = [StudentStatusResponseDTO(**student.dict()) for student in school.students]
                    teacher_attendance = [TeacherStatusResponseDTO(**teacher.dict()) for teacher in school.teachers]

                    school_attendance = SchoolStatusResponseDTO( 
                        school_id=school.school_id,
                        students=student_attendance,
                        teachers=teacher_attendance
                        )
                    
                    school_attendances.append(school_attendance)

                attendance_response = AttendanceResponseDTO(
                    id= attendance.id,
                    date=attendance.date,
                    schools=school_attendances
                )
                attendances.append(attendance_response)
            
            return attendances
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving all attendances: {str(e)}")

    async def get_attendance_by_date(self, date: str) -> Optional[AttendanceResponseDTO]:
        if not self.validate_input(date):
            raise HTTPException(status_code=400, detail="Invalid input for date")
        self.logger.info(f"Retrieving attendance for date: {date}")
        try:
            attendance = await self.attendance_repository.get_attendance_by_date(date)
            school_attendances=[]
            for school in attendance.schools:
                    student_attendance = [StudentStatusResponseDTO(**student.dict()) for student in school.students]
                    teacher_attendance = [TeacherStatusResponseDTO(**teacher.dict()) for teacher in school.teachers]

                    school_attendance = SchoolStatusResponseDTO( 
                        school_id=school.school_id,
                        students=student_attendance,
                        teachers=teacher_attendance
                        )
                    
                    school_attendances.append(school_attendance)

            attendance_response = AttendanceResponseDTO(
                    id= attendance.id,
                    date=attendance.date,
                    schools=school_attendances
                )
            return attendance_response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving attendance by date: {str(e)}")

    async def get_student_attendance(self, student_id: str) -> List[AttendanceResponseDTO]:
        if not self.validate_input(student_id):
            raise HTTPException(status_code=400, detail="Invalid input for student_id")
        
        self.logger.info(f"Retrieving attendance for student: {student_id}")
        
        try:
            attendances = await self.attendance_repository.get_student_attendance(student_id)
            self.logger.debug(f"Retrieved attendances: {attendances}")
            
            attendance_response_list = []
            
            for attendance in attendances:
                schools_response = []
                for school in attendance.schools:
                    student_status = next(
                        (student for student in school.students 
                        if student.student_id == student_id),
                        None
                    )
                    
                    if student_status:
                        student_response = StudentStatusResponseDTO(
                            student_id=str(student_status.student_id),
                            status=student_status.status,
                            remarks=student_status.remarks
                        )
                        
                        school_response = SchoolStatusResponseDTO(
                            school_id=str(school.school_id),
                            students=[student_response],
                        )
                        schools_response.append(school_response)
                
                if schools_response:  
                    attendance_response = AttendanceResponseDTO(
                        id = attendance.id,
                        date=attendance.date,
                        schools=schools_response
                    )
                    attendance_response_list.append(attendance_response)
            
            return attendance_response_list
        
        except Exception as e:
            self.logger.error(f"Error retrieving student attendance: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error retrieving student attendance: {str(e)}")

    async def get_teacher_attendance(self, teacher_id: str) -> List[AttendanceResponseDTO]:
        if not self.validate_input(teacher_id):
            raise HTTPException(status_code=400, detail="Invalid input for teacher_id")

        self.logger.info(f"Retrieving attendance for teacher: {teacher_id}")

        try:
            attendances = await self.attendance_repository.get_teacher_attendance(teacher_id)
            self.logger.debug(f"Retrieved attendances: {attendances}")

            attendance_response_list = []

            for attendance in attendances:
                schools_response = []
                for school in attendance.schools:
                    teacher_status = next(
                        (teacher for teacher in school.teachers
                        if teacher.teacher_id == teacher_id),
                        None
                    )

                    if teacher_status:
                        teacher_response = TeacherStatusResponseDTO(
                            teacher_id=str(teacher_status.teacher_id),
                            status=teacher_status.status,
                            remarks=teacher_status.remarks
                        )

                        school_response = SchoolStatusResponseDTO(
                            school_id=str(school.school_id),
                            teachers=[teacher_response],
                        )
                        schools_response.append(school_response)

                if schools_response:  # Only add attendance if the teacher was found
                    attendance_response = AttendanceResponseDTO(
                        id = attendance.id,
                        date=attendance.date,
                        schools=schools_response
                    )
                    attendance_response_list.append(attendance_response)

            return attendance_response_list

        except Exception as e:
            self.logger.error(f"Error retrieving teacher attendance: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error retrieving teacher attendance: {str(e)}")
        