import io
from fastapi import HTTPException, UploadFile
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload

class FileService:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'service_account.json'
    GALLERY_FOLDER_ID = "1W177hJM__jF2mVfMRwFc1XE2vk9SjuEB"  
    IMAGES_FOLDER_NAME = "images"
    VIDEOS_FOLDER_NAME = "videos"

    VALID_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"}
    VALID_VIDEO_EXTENSIONS = {"mp4", "avi", "mov", "wmv", "flv", "mkv"}

    @staticmethod
    def authenticate():
        creds = service_account.Credentials.from_service_account_file(FileService.SERVICE_ACCOUNT_FILE, scopes=FileService.SCOPES)
        return creds

    @staticmethod
    def is_valid_image_extension(filename: str) -> bool:
        extension = filename.split(".")[-1].lower()
        return extension in FileService.VALID_IMAGE_EXTENSIONS

    @staticmethod
    def is_valid_video_extension(filename: str) -> bool:
        extension = filename.split(".")[-1].lower()
        return extension in FileService.VALID_VIDEO_EXTENSIONS

    @staticmethod
    async def upload_file(file: UploadFile):
        creds = FileService.authenticate()
        service = build('drive', 'v3', credentials=creds)

        if FileService.is_valid_image_extension(file.filename):
            folder = "images"
            mime_type = "image/" + file.filename.split(".")[-1].lower()
        elif FileService.is_valid_video_extension(file.filename):
            folder = "videos"
            mime_type = "video/" + file.filename.split(".")[-1].lower()
        else:
            raise HTTPException(status_code=400, detail="Invalid file extension. Only image and video files are allowed.")

        folder_id = FileService.get_or_create_folder(service, folder)

        try:
            file_metadata = {
                'name': file.filename,
                'parents': [folder_id]
            }
            
            file_content = await file.read()
            media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype=mime_type, resumable=True)
            
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()

            return {
                "message": f"File uploaded successfully to {folder} folder in Google Drive",
                "file_id": file.get('id'),
                "web_view_link": file.get('webViewLink')
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file: {str(e)}")

    @staticmethod
    def get_or_create_folder(service, folder_name):
        results = service.files().list(
            q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and '{FileService.GALLERY_FOLDER_ID}' in parents",
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        folders = results.get('files', [])

        if not folders:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [FileService.GALLERY_FOLDER_ID]
            }
            folder = service.files().create(body=file_metadata, fields='id').execute()
            return folder.get('id')
        
        return folders[0]['id']

