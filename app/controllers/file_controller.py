import base64
import configparser
import io
from fastapi import APIRouter, HTTPException, Response, UploadFile, File
from typing import List
from fastapi.responses import StreamingResponse
from app.service.file_service import FileService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger

file_route = APIRouter()
config = configparser.ConfigParser()
config.read('config.ini')
logger = get_logger()

@file_route.post("/files/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload multiple files to S3.
    """
    logger.info("CALLED: POST - Uploading files")
    try:
        result = await FileService.save_uploaded_files(files)
        logger.info(f"Files uploaded successfully. Files: {result}")
        return get_response(status="success", status_code=200, message="Files uploaded successfully", data=result)
    except HTTPException as he:
        logger.error(f"HTTP Exception during file upload: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred during file upload: {str(e)}")
    
@file_route.get("/files/download/{filename}")
async def download_file(filename: str):
    logger.info(f"ENDPOINT CALLED: /files/download/{filename}")
    folder = config['aws']['aws_s3_image_path']
    file_path = f"{folder}/{filename}"
    
    try:
        file_content = await FileService.download_from_s3(file_path)
        if not file_content:
            raise HTTPException(status_code=404, detail="File not found")
        
        return Response(content=file_content, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={filename}"})
    except HTTPException as he:
        logger.error(f"HTTPException during file download: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"Unexpected error during file download: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error during file download: {str(e)}")

@file_route.post("/files/download")
async def download_files(filenames: List[str]):
    logger.info("CALLED: POST - Retrieving files for display")
    try:
        result = await FileService.download_files(filenames)
        files_for_display = []
        failed_retrievals = []

        for item in result:
            if "error" in item:
                failed_retrievals.append(item)
            else:
                # Encode the binary content to base64
                base64_content = base64.b64encode(item["content"]).decode("utf-8")
                files_for_display.append({
                    "filename": item["filename"],
                    "content_type": item["content_type"],
                    "file_type": item["file_type"],
                    "content": f"data:{item['content_type']};base64,{base64_content}"
                })
        
        logger.info(f"Files retrieved successfully. Successful: {len(files_for_display)}, Failed: {len(failed_retrievals)}")
        
        return get_response(
            status="success", 
            status_code=200, 
            message="Files retrieval process completed",
            data={
                "files_for_display": files_for_display,
                "failed_retrievals": failed_retrievals
            }
        )
    except HTTPException as he:
        logger.error(f"HTTP Exception during file retrieval: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"Error during file retrieval: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred during file retrieval: {str(e)}")

