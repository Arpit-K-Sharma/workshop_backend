import cloudinary
import cloudinary.uploader
from cloudinary import api
from cloudinary.utils import cloudinary_url
from fastapi import HTTPException, UploadFile
from dotenv import load_dotenv
import os

class CloudinaryFileService:
    load_dotenv()

    # Valid extensions
    VALID_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"}
    VALID_VIDEO_EXTENSIONS = {"mp4", "avi", "mov", "wmv", "flv", "mkv"}

    # API name, key and secret
    cloudinary_api_name = os.getenv('CLOUDINARY_NAME')
    cloudinary_api_key = os.getenv('CLOUDINARY_API_KEY')
    cloudinary_api_secret = os.getenv('CLOUDINARY_API_SECRET')

    @staticmethod
    def configure_cloudinary():
        cloudinary.config(
            cloud_name=CloudinaryFileService.cloudinary_api_name,
            api_key=CloudinaryFileService.cloudinary_api_key,
            api_secret=CloudinaryFileService.cloudinary_api_secret,
            secure=True
        )

    @staticmethod
    def is_valid_image_extension(filename: str) -> bool:
        extension = filename.split(".")[-1].lower()
        return extension in CloudinaryFileService.VALID_IMAGE_EXTENSIONS

    @staticmethod
    def is_valid_video_extension(filename: str) -> bool:
        extension = filename.split(".")[-1].lower()
        return extension in CloudinaryFileService.VALID_VIDEO_EXTENSIONS

    @staticmethod
    async def ensure_gallery_folder():
        CloudinaryFileService.configure_cloudinary()
        
        # Check if gallery folder exists, create if it doesn't
        try:
            result = cloudinary.api.root_folders()
            if not any(folder['name'] == 'gallery' for folder in result['folders']):
                api.create_folder('gallery')
            
            # Ensure images and videos folders exist inside gallery
            subfolders = cloudinary.api.subfolders('gallery')['folders']
            if not any(folder['name'] == 'images' for folder in subfolders):
                api.create_folder('gallery/images')
            if not any(folder['name'] == 'videos' for folder in subfolders):
                api.create_folder('gallery/videos')
        except Exception as e:
            print(f"Error ensuring gallery folder structure: {str(e)}")

    @staticmethod
    async def upload_file(file: UploadFile):
        await CloudinaryFileService.ensure_gallery_folder()

        if CloudinaryFileService.is_valid_image_extension(file.filename):
            folder = "gallery/images"
        elif CloudinaryFileService.is_valid_video_extension(file.filename):
            folder = "gallery/videos"
        else:
            raise HTTPException(status_code=400, detail="Invalid file extension. Only image and video files are allowed.")

        try:
            # Read file content
            file_content = await file.read()
            
            # Upload file to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file_content,
                folder=folder,
                resource_type="auto",
                public_id=file.filename.split('.')[0],  # Use filename without extension as public_id
                overwrite=True
            )

            # Generate optimized URL
            optimized_url, _ = cloudinary_url(
                upload_result['public_id'],
                format="auto",
                quality="auto",
                secure=True
            )

            return {
                "message": f"File uploaded successfully to {folder} folder in Cloudinary",
                "file_id": upload_result['public_id'],
                "original_url": upload_result['secure_url'],
                "optimized_url": optimized_url
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file: {str(e)}")