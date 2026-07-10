from fastapi import UploadFile,HTTPException,status
from app.core.config import settings
import magic
import os
import shutil
import hashlib
from pathlib import Path
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.upload import Upload, UploadStatus
from app.tasks.upload_tasks import process_upload

async def validating_file(uploadedFile : UploadFile) -> str:
    #Validating the file
    if uploadedFile.size > settings.MAX_UPLOAD_SIZE_BYTES:
         raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum allowed size is {settings.MAX_UPLOAD_SIZE_BYTES / (1024*1024)}MB."
        )
    
    header_bytes = await uploadedFile.read(2048)
    await uploadedFile.seek(0) 

    detected_mime = magic.from_buffer(header_bytes, mime=True)

    if detected_mime not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {detected_mime}. Only standard media files are allowed."
        )
    
    return detected_mime
    
async def store_file(uploadedFile : UploadFile):
    media_id = str(uuid4())
    folder_path = Path(settings.UPLOAD_DIR) / media_id
    folder_path.mkdir(parents=True, exist_ok=True)

    extension = Path(uploadedFile.filename).suffix.lower()

    stored_filename = f"{media_id}{extension}"
    file_path = folder_path / stored_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploadedFile.file, buffer)

    return file_path
    

async def calculate_hash(uploadedFile : UploadFile) -> str:
    sha256_hash = hashlib.sha256()
    
    # Read chunks asynchronously
    while chunk := await uploadedFile.read(65536):
        sha256_hash.update(chunk)
        
    await uploadedFile.seek(0) # Reset pointer
    return sha256_hash.hexdigest()

def upload_media(
        db: Session,uploadedFile : UploadFile, 
        detected_mime : str,sha_hash : str,
        file_path : str
    ):
    
    upload = Upload(
        original_filename=uploadedFile.filename,
        stored_filename=str(file_path).split('/')[-1],
        file_path=str(file_path),
        media_type=uploadedFile.content_type.split('/',1)[0],
        mime_type=detected_mime,
        file_size=uploadedFile.size,
        sha256_hash=sha_hash,
        status=UploadStatus.UPLOADED,
        language=None,
    )

    db.add(upload)
    db.commit()
    db.refresh(upload)

    return upload

def file_exists(sha_hash:str,db:Session):
    query = select(Upload).where(Upload.sha256_hash == sha_hash)
    existing_file = db.scalar(query)
    return existing_file

async def create_upload(uploadedFile : UploadFile,db : Session):
        detected_mime = await validating_file(uploadedFile)
        sha_hash = await calculate_hash(uploadedFile)
        existing_file =  file_exists(sha_hash,db)
        
        if existing_file:
            return {
                "upload_id" : existing_file.id,
                "status" : existing_file.status,
                "media_type": existing_file.media_type,
                "file_path":existing_file.file_path,
                "is_duplication":True,
                "message":"File Already exists in the database."
            }
        
        file_path = await store_file(uploadedFile)
        uploaded_file = upload_media(db,uploadedFile,detected_mime,sha_hash,file_path)
        
        #Queueing the file for processing 
        uploaded_file.status = UploadStatus.QUEUED
        db.commit()
        db.refresh(uploaded_file)

        process_upload.delay(uploaded_file.id)
        
        return {
            "upload_id" : uploaded_file.id,
            "status" : uploaded_file.status,
            "media_type":uploaded_file.media_type,
            "file_path":uploaded_file.file_path,
            "is_duplication":False,
            "message":"File uploaded and stored successfully."
        }
    
    
def get_upload_status( upload_id:int,db: Session):
    query = select(Upload).where(Upload.id== upload_id)
    response = db.scalar(query)

    return response