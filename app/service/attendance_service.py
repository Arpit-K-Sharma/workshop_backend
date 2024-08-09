from datetime import datetime
from typing import List, Optional
from bson import DBRef, ObjectId
from fastapi import HTTPException
from app.repositories.attendance_repo import AttendanceRepository
from app.models.attendance_model import Attendance, SchoolStatus, ClassStatus, StudentStatus
from app.dto.attendance_dto import AttendanceDTO, AttendanceResponseDTO, StudentStatusResponseDTO, ClassStatusResponseDTO, SchoolStatusResponseDTO

class AttendanceService:
    def __init__(self, repository: AttendanceRepository):
        self.attendance_repository = repository

    def validate_input(self, input_value):
        if input_value is None or input_value == "":
            return False
        return True

    async def create_attendance(self, attendance_dto: AttendanceDTO) -> str:
        if not self.validate_input(attendance_dto.date):
            raise HTTPException(status_code=400, detail="Invalid input for date")

        try:
            existing_attendance = await self.attendance_repository.get_attendance_by_date(attendance_dto.date)
            if existing_attendance:
                existing_attendance = AttendanceDTO(**existing_attendance.dict())
                # Update existing attendance
                for school_dto in attendance_dto.schools:
                    school_exists = False
                    for school in existing_attendance.schools:
                        if school.school_id == school_dto.school_id:
                            school_exists = True
                            # Update classes
                            for class_dto in school_dto.classes:
                                class_exists = False
                                for class_status in school.classes:
                                    if class_status.class_id == class_dto.class_id:
                                        class_exists = True
                                        # Update students
                                        for student_dto in class_dto.students:
                                            student_exists = False
                                            for student in class_status.students:
                                                if student.student_id == student_dto.student_id:
                                                    student.status = student_dto.status
                                                    student.remarks = student_dto.remarks
                                                    student_exists = True
                                                    break
                                            if not student_exists:
                                                class_status.students.append(student_dto)
                                        break
                                if not class_exists:
                                    school.classes.append(class_dto)
                            break
                    if not school_exists:
                        existing_attendance.schools.append(school_dto)
                return await self.attendance_repository.upsert_attendance(existing_attendance)
            else:
                # Create new attendance
                attendance = Attendance(**attendance_dto.dict())
                return await self.attendance_repository.create_attendance(attendance)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating attendance: {str(e)}")


    async def get_all_attendances(self) -> List[AttendanceResponseDTO]:
        try:
            attendances = await self.attendance_repository.get_all_attendances()
            return [self.convert_to_response_dto(attendance) for attendance in attendances]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving all attendances: {str(e)}")

    async def get_attendance_by_date(self, date: str) -> Optional[AttendanceResponseDTO]:
        if not self.validate_input(date):
            raise HTTPException(status_code=400, detail="Invalid input for date")
        try:
            attendance = await self.attendance_repository.get_attendance_by_date(date)
            if attendance:
                return self.convert_to_response_dto(attendance)
            return None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving attendance by date: {str(e)}")

    async def get_student_attendance(self, student_id: str) -> List[AttendanceResponseDTO]:
        if not self.validate_input(student_id):
            raise HTTPException(status_code=400, detail="Invalid input for student_id")
        try:
            attendances = await self.attendance_repository.get_student_attendance(student_id)
            return [self.convert_to_response_dto(attendance) for attendance in attendances]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving student attendance: {str(e)}")

    async def get_teacher_attendance(self, teacher_id: str) -> List[AttendanceResponseDTO]:
        if not self.validate_input(teacher_id):
            raise HTTPException(status_code=400, detail="Invalid input for teacher_id")
        try:
            attendances = await self.attendance_repository.get_teacher_attendance(teacher_id)
            return [self.convert_to_response_dto(attendance) for attendance in attendances]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving teacher attendance: {str(e)}")

    def convert_to_response_dto(self, attendance: Attendance) -> AttendanceResponseDTO:
        school_attendances = [
            self.convert_school_status_to_response_dto(school)
            for school in attendance.schools
        ]
        return AttendanceResponseDTO(
            id=str(attendance.id),
            date=attendance.date,
            schools=school_attendances
        )

    def convert_school_status_to_response_dto(self, school_status: SchoolStatus) -> SchoolStatusResponseDTO:
        class_attendances = [
            self.convert_class_status_to_response_dto(class_status)
            for class_status in school_status.classes
        ]
        return SchoolStatusResponseDTO(
            school_id=str(school_status.school_id),
            classes=class_attendances
        )

    def convert_class_status_to_response_dto(self, class_status: ClassStatus) -> ClassStatusResponseDTO:
        student_attendances = [
            self.convert_student_status_to_response_dto(student)
            for student in class_status.students
        ]
        return ClassStatusResponseDTO(
            class_id=str(class_status.class_id),
            students=student_attendances
        )

    def convert_student_status_to_response_dto(self, student_status: StudentStatus) -> StudentStatusResponseDTO:
        return StudentStatusResponseDTO(
            student_id=str(student_status.student_id),
            status=student_status.status,
            remarks=student_status.remarks
        )
