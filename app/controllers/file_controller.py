from fastapi import APIRouter, UploadFile
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
