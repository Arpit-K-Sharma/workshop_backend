import datetime
import os
from fastapi import APIRouter, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from app.config.logger_config import get_logger
from app.service.file_service import FileService
from app.service.cloudinary_file_service import CloudinaryFileService
from app.utils.response_util import get_response

file_route = APIRouter()
logger = get_logger()

@file_route.post("/file/upload")
async def upload_file(file: UploadFile):
    logger.info(f"ENDPOINT CALLED: POST /file/upload - Uploading file")
    result = await FileService.upload_file(file)
    logger.info(f"File uploaded successfully. File: {result}")
    return get_response(status="success", status_code=200, message=result)

@file_route.get("/download/{file_id}")
async def download_file(file_id: str):
    logger.info(f"ENDPOINT CALLED: GET /download/{file_id} - Downloading file")
    file_data = await FileService.download_file(file_id)
    logger.info(f"File downloaded successfully.")

    # If the file_data is already a Response object (for text files)
    if isinstance(file_data, Response):
        return file_data

    # For binary files (returned as a dictionary with base64 encoded content)
    return JSONResponse(content={
        "file_name": file_data["file_name"],
        "mime_type": file_data["mime_type"],
        "content_url": file_data["content_url"]  # This is the base64 encoded content
    })


