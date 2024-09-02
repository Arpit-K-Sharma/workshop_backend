from fastapi import FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.config.db_config import mongodb,MONGO_URI,DATABASE_NAME
from app.controllers.feedback_controller import feedback_route
from app.controllers.attendance_controller import attendance_route
from app.controllers.file_controller import file_route
from app.controllers.teacher_controller import teacher_route
from app.controllers.student_controller import student_route
from app.controllers.course_controller import course_route
from app.controllers.event_controller import event_route
from app.controllers.school_controller import school_route
from app.controllers.hof_controller import hof_route
from app.controllers.class_controller import class_route
from app.controllers.calendar_controller import calendar_route
from app.controllers.assignmentDashboard_controller import assignment_route
from app.controllers.auth_controller import auth_route
from app.config.logger_config import get_logger

app = FastAPI()
logger = get_logger()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    return {"message": "Welcome to Workshop"}



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to MongoDB
    await mongodb.connect(MONGO_URI, DATABASE_NAME)

    # Check if the admin collection is empty
    try:
        admin_count = await mongodb.collections['admin'].count_documents({})
        if admin_count == 0:
            admin_data = {
                "email": "admin@gmail.com",
                "password": "admin123",
                "role": "ADMIN",
            }
            await mongodb.collections['admin'].insert_one(admin_data)
            logger.info("Admin data added to the collection.")
        
    except Exception as e:
        logger.error(f"Error inserting admin data: {e}")

    yield

app.router.lifespan_context = lifespan

# Controllers
app.include_router(file_route, tags=["File"])
app.include_router(teacher_route, tags=["Teacher"])
app.include_router(student_route, tags=["Student"])
app.include_router(course_route,tags=["Course"])
app.include_router(event_route,tags=["Event"])
app.include_router(school_route,tags=["School"])
app.include_router(attendance_route, tags=["Attendance"])
app.include_router(feedback_route, tags=["Feedback"])
app.include_router(hof_route,tags=["HOF"])
app.include_router(class_route,tags=["Class"])
app.include_router(calendar_route,tags=["calendar"])
app.include_router(assignment_route,tags=["assignment"])
app.include_router(auth_route,tags=["auth"])



