from fastapi import APIRouter, File, UploadFile, Request, HTTPException, Response
import os
import aiofiles
import magic
from app.core.config import settings

upload_router = APIRouter()

def sanitize_filename(filename: str) -> str:
    """Sanitize filename and validate extension"""
    clean_name = os.path.basename(filename).replace('"', '')
    ext = os.path.splitext(clean_name)[1].lower()
    
    if ext not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {ext}. Allowed types: {', '.join(settings.allowed_extensions)}"
        )
    
    return clean_name

async def validate_image_content(contents: bytes) -> str:
    """Validate actual file content using magic"""
    try:
        mime_type = magic.from_buffer(contents, mime=True)
        if not mime_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid image format detected: {mime_type}"
            )
        return mime_type
    except Exception as e:
        raise HTTPException(status_code=400, detail="Could not validate file content")

@upload_router.post("/upload/image")
async def upload_image(
    request: Request,
    file: UploadFile = File(...)
):
    
    # File not found
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Check content type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Check file size
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file")
    if len(contents) > settings.max_file_size:
        raise HTTPException(status_code=413, detail=f"File too large. Maximum size: {settings.max_file_size / 1024 / 1024:.1f}MB")
    
    # Reset file pointer to beginning after reading
    await file.seek(0)
    
    # Validate image content
    mime_type = await validate_image_content(contents)

    # Sanitize filename
    filename = sanitize_filename(file.filename)

    # Define output directory
    os.makedirs(settings.upload_dir, exist_ok=True)
    file_path = os.path.join(settings.upload_dir, filename)

    # Handle filename conflicts
    counter = 1
    base_name, ext = os.path.splitext(filename)
    while os.path.exists(file_path):
        filename = f"{base_name}_{counter}{ext}"
        file_path = os.path.join(settings.upload_dir, filename)
        counter += 1

    # Save file using async file operations
    async with aiofiles.open(file_path, "wb") as f:
        # Read file in chunks
        while chunk := await file.read(1024):
            await f.write(chunk)

    # Get request ID from middleware (if set)
    request_id = getattr(request.state, "request_id", "-")

    # Response with file details
    headers = {
        "Content-Type": mime_type,
        "Content-Disposition": f'inline; filename="{filename}"',
        "X-Request-ID": request_id
    }
    return Response(content=contents, headers=headers, media_type=mime_type)