from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class StudentAttendanceDTO(BaseModel):
    student_id: str
    student_name : str
    status: str
    remarks: Optional[str] = None

class ClassAttendanceDTO(BaseModel):
    class_id: str
    date: str
    students: List[StudentAttendanceDTO]

class StudentDailyAttendanceDTO(BaseModel):
    date: str
    status: str
    remarks: Optional[str] = None

class StudentMonthlyAttendanceDTO(BaseModel):
    student_id: str
    attendances: List[StudentDailyAttendanceDTO]

class ClassMonthlyAttendanceDTO(BaseModel):
    class_id: str
    attendances: List[ClassAttendanceDTO]

class StudentCourseMonthlyAttendanceDTO(BaseModel):
    student_id: str
    course_id: str
    attendances: List[StudentDailyAttendanceDTO]