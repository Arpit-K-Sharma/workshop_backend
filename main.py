import logging
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.config.db_config import mongodb,MONGO_URI,DATABASE_NAME

app = FastAPI()

# CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/workshop")
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
                "username": "admin",
                "password": "admin123",
                "role": "ADMIN",
            }
            await mongodb.collections['admin'].insert_one(admin_data)
            logging.info("Admin data added to the collection.")
        
    except Exception as e:
        logging.error(f"Error inserting admin data: {e}")

    yield

app.router.lifespan_context = lifespan

