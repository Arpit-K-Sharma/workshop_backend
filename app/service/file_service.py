import base64
from multiprocessing import get_logger
import os
from fastapi import HTTPException, UploadFile
import configparser
import boto3
from botocore.exceptions import ClientError
from fastapi.responses import StreamingResponse
from starlette.status import HTTP_415_UNSUPPORTED_MEDIA_TYPE
import uuid
import asyncio
from typing import List

config = configparser.ConfigParser()
config.read('config.ini')
logger = get_logger()

class FileService:
    ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
    ALLOWED_VIDEO_EXTENSIONS = [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv"]

    @staticmethod
    def get_s3_client():
        return boto3.client(
            's3',
            aws_access_key_id=config['aws']['aws_access_key_id'],
            aws_secret_access_key=config['aws']['aws_secret_access_key'],
            region_name=config['aws']['aws_region_name']
        )

    @staticmethod
    def is_allowed_file(filename: str) -> bool:
        return any(filename.lower().endswith(ext) for ext in FileService.ALLOWED_IMAGE_EXTENSIONS + FileService.ALLOWED_VIDEO_EXTENSIONS)

    @staticmethod
    def get_file_type(filename: str) -> str:
        if any(filename.lower().endswith(ext) for ext in FileService.ALLOWED_IMAGE_EXTENSIONS):
            return "image"
        elif any(filename.lower().endswith(ext) for ext in FileService.ALLOWED_VIDEO_EXTENSIONS):
            return "video"
        else:
            raise ValueError("Unsupported file type")

    @staticmethod
    async def upload_to_s3(file_content: bytes, file_path: str):
        s3 = FileService.get_s3_client()
        bucket_name = config['aws']['aws_bucket_name']
        try:
            s3.put_object(
                Bucket=bucket_name,
                Key=file_path,
                Body=file_content
            )
            print(f"Uploaded: {file_path}")
        except ClientError as e:
            print(f"Error during S3 upload: {e}")
            raise

    @staticmethod
    async def download_from_s3(file_path: str) -> dict:
        s3 = FileService.get_s3_client()
        bucket_name = config["aws"]["aws_bucket_name"]
        
        if not bucket_name:
            raise HTTPException(status_code=500, detail="AWS bucket name is not configured")

        try:
            # Get file from S3
            file = s3.get_object(Bucket=bucket_name, Key=file_path)

            # Read file content
            file_content = file['Body'].read()
            file_name = os.path.basename(file_path)

            logger.info(f"File downloaded successfully from S3: {file_path}")
            return file_content
        
        except ClientError as e:
            logger.error(f"Error during S3 download: {e}")
            raise HTTPException(status_code=500, detail=f"Error during S3 download: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during S3 download: {e}")
            raise HTTPException(status_code=500, detail=f"Unexpected error during S3 download: {e}")
        
    @staticmethod
    async def internal_download_from_s3(file_path: str) -> dict:
        s3 = FileService.get_s3_client()
        bucket_name = config["aws"]["aws_bucket_name"]
        
        if not bucket_name:
            raise HTTPException(status_code=500, detail="AWS bucket name is not configured")

        try:
            # Get file from S3
            file = s3.get_object(Bucket=bucket_name, Key=file_path)

            # Read file content
            file_content = file['Body'].read()
            file_name = os.path.basename(file_path)

            logger.info(f"File downloaded successfully from S3: {file_path}")
            return {"file_name":file_content}
        
        except ClientError as e:
            logger.error(f"Error during S3 download: {e}")
            raise HTTPException(status_code=500, detail=f"Error during S3 download: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during S3 download: {e}")
            raise HTTPException(status_code=500, detail=f"Unexpected error during S3 download: {e}")


    @staticmethod
    async def save_uploaded_files(files: List[UploadFile]):

        if not files:
            raise HTTPException(status_code=400, detail="No files provided")

        upload_tasks = []
        results = []
        for file in files:
            if not FileService.is_allowed_file(file.filename):
                raise HTTPException(
                    status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    detail=f"File {file.filename} is not allowed. Only images and videos are permitted."
                )
            

            file_type = FileService.get_file_type(file.filename)
            folder = config['aws'][f'aws_s3_{file_type}_path']

            unique_filename = f"{file.filename}"
            file_path = f"{folder}/{unique_filename}"

            file_content = await file.read()
            
            asyncio.create_task(FileService.upload_to_s3(file_content, file_path))

            results.append({
                "uploaded_filename": unique_filename,
                "file_type": file_type
            })

            

        return results
    




    @staticmethod
    async def download_files(filenames: List[str]):
        if not filenames:
            raise HTTPException(status_code=400, detail="No filenames provided")

        s3 = FileService.get_s3_client()
        bucket_name = config['aws']['aws_bucket_name']
        results = []
        files_for_display = []
        failed_retrievals = []
        for filename in filenames:
            try:
                file_type = FileService.get_file_type(filename)
                folder = config['aws'][f'aws_s3_{file_type}_path']
                file_path = f"{folder}/{filename}"

                # Get file from S3
                file = s3.get_object(Bucket=bucket_name, Key=file_path)
                
                # Read file content
                file_content = file['Body'].read()
                
                # Determine content type
                content_type = file['ContentType'] if 'ContentType' in file else 'application/octet-stream'
                
                results.append({
                    "filename": filename,
                    "content": file_content,
                    "content_type": content_type,
                    "file_type": file_type
                })

            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchKey':
                    results.append({
                        "filename": filename,
                        "error": "File not found"
                    })
                else:
                    results.append({
                        "filename": filename,
                        "error": f"S3 download failed: {str(e)}"
                    })
            except Exception as e:
                results.append({
                    "filename": filename,
                    "error": f"An error occurred: {str(e)}"
                })

        for item in results:
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
        return files_for_display
    


    # @staticmethod
    # async def get_file_details(filenames: List[str]):
    #     if not filenames:
    #         return []

    #     s3 = FileService.get_s3_client()
    #     bucket_name = config['aws']['aws_bucket_name']
        
    #     results = []
    #     for filename in filenames:
    #         try:
    #             file_type = FileService.get_file_type(filename)
    #             folder = config['aws'][f'aws_s3_{file_type}_path']
    #             file_path = f"{folder}/{filename}"

    #             # Get file metadata from S3
    #             file_metadata = s3.head_object(Bucket=bucket_name, Key=file_path)
                
    #             # Generate a pre-signed URL for the file
    #             url = s3.generate_presigned_url(
    #                 'get_object',
    #                 Params={'Bucket': bucket_name, 'Key': file_path},
    #                 ExpiresIn=3600  # URL expires in 1 hour
    #             )
                
    #             results.append({
    #                 "filename": filename,
    #                 "url": url,
    #                 "content_type": file_metadata.get('ContentType', 'application/octet-stream'),
    #                 "file_type": file_type,
    #                 "size": file_metadata.get('ContentLength', 0)
    #             })

    #         except Exception as e:
    #             results.append({
    #                 "filename": filename,
    #                 "error": f"An error occurred: {str(e)}"
    #             })

    #     return results









































































































# Google Drive code
# import base64
# import io
# from fastapi import HTTPException, Response, UploadFile
# from aiocache import cached
# from aiocache.serializers import JsonSerializer
# from cachetools import TTLCache
# from fastapi.responses import StreamingResponse
# from googleapiclient.discovery import build
# from fastapi.responses import JSONResponse
# from google.oauth2 import service_account
# from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

# cache = TTLCache(maxsize=100, ttl=3600)

# class FileService:
#     SCOPES = ['https://www.googleapis.com/auth/drive']
#     SERVICE_ACCOUNT_FILE = 'service_account.json'
#     GALLERY_FOLDER_ID = "1W177hJM__jF2mVfMRwFc1XE2vk9SjuEB"  
#     IMAGES_FOLDER_NAME = "images"
#     VIDEOS_FOLDER_NAME = "videos"

#     VALID_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"}
#     VALID_VIDEO_EXTENSIONS = {"mp4", "avi", "mov", "wmv", "flv", "mkv"}

#     @staticmethod
#     def authenticate():
#         creds = service_account.Credentials.from_service_account_file(FileService.SERVICE_ACCOUNT_FILE, scopes=FileService.SCOPES)
#         return creds

#     @staticmethod
#     def is_valid_image_extension(filename: str) -> bool:
#         extension = filename.split(".")[-1].lower()
#         return extension in FileService.VALID_IMAGE_EXTENSIONS

#     @staticmethod
#     def is_valid_video_extension(filename: str) -> bool:
#         extension = filename.split(".")[-1].lower()
#         return extension in FileService.VALID_VIDEO_EXTENSIONS

#     @staticmethod
#     async def upload_file(file: UploadFile):
#         creds = FileService.authenticate()
#         service = build('drive', 'v3', credentials=creds)

#         if FileService.is_valid_image_extension(file.filename):
#             folder = "images"
#             mime_type = "image/" + file.filename.split(".")[-1].lower()
#         elif FileService.is_valid_video_extension(file.filename):
#             folder = "videos"
#             mime_type = "video/" + file.filename.split(".")[-1].lower()
#         else:
#             raise HTTPException(status_code=400, detail="Invalid file extension. Only image and video files are allowed.")

#         folder_id = FileService.get_or_create_folder(service, folder)

#         try:
#             file_metadata = {
#                 'name': file.filename,
#                 'parents': [folder_id]
#             }
            
#             file_content = await file.read()
#             media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype=mime_type, resumable=True)
            
#             file = service.files().create(
#                 body=file_metadata,
#                 media_body=media,
#                 fields='id, webViewLink'
#             ).execute()

#             return {
#                 "message": f"File uploaded successfully to {folder} folder in Google Drive",
#                 "file_id": file.get('id'),
#                 "web_view_link": file.get('webViewLink')
#             }
        
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file: {str(e)}")

#     @staticmethod
#     def get_or_create_folder(service, folder_name):
#         results = service.files().list(
#             q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and '{FileService.GALLERY_FOLDER_ID}' in parents",
#             spaces='drive',
#             fields='files(id, name)'
#         ).execute()
#         folders = results.get('files', [])

#         if not folders:
#             file_metadata = {
#                 'name': folder_name,
#                 'mimeType': 'application/vnd.google-apps.folder',
#                 'parents': [FileService.GALLERY_FOLDER_ID]
#             }
#             folder = service.files().create(body=file_metadata, fields='id').execute()
#             return folder.get('id')
        
#         return folders[0]['id']


#     @staticmethod
#     @cached(ttl=3600, serializer=JsonSerializer())
#     async def download_file(file_id: str):
#         if file_id in cache:
#             return cache[file_id]
        
#         creds = FileService.authenticate()
#         service = build('drive', 'v3', credentials=creds)
        
#         try:
#             # Get the file metadata
#             file_metadata = service.files().get(fileId=file_id).execute()
#             file_name = file_metadata['name']
#             mime_type = file_metadata['mimeType']
            
#             # Download the file content
#             request = service.files().get_media(fileId=file_id)
#             file_content = io.BytesIO()
#             downloader = MediaIoBaseDownload(file_content, request)
#             done = False
#             while not done:
#                 _, done = downloader.next_chunk()
            
#             file_content.seek(0)
#             content = file_content.getvalue()

#             # Encode the content as base64
#             encoded_content = base64.b64encode(content).decode('utf-8')
            
#             # Create a data URL
#             data_url = f"data:{mime_type};base64,{encoded_content}"

#             result = JSONResponse(content={
#                 "file_name": file_name,
#                 "mime_type": mime_type,
#                 "content_url": data_url
#             })

#             cache[file_id] = result

#             return result
        
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"An error occurred while downloading the file: {str(e)}")