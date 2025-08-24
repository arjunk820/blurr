from fastapi import APIRouter, File, UploadFile, Request, HTTPException, Response
import os
import aiofiles

upload_router = APIRouter()
MAX_SIZE = 5 * 1024 * 1024 # 5 MB

def sanitize_filename(filename):
    return os.path.basename(filename).replace('"', '')

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
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    
    # Reset file pointer to beginning after reading
    await file.seek(0)
    
    # Sanitize filename
    filename = sanitize_filename(file.filename)

    app_dir = os.path.join(os.getcwd(), 'app')
    if not os.path.exists(app_dir):
        app_dir = os.path.join(os.path.dirname(os.getcwd()), 'app')
    
    output_dir = os.path.join(app_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)

    # Save file using async file operations
    async with aiofiles.open(file_path, "wb") as f:
        # Read file in chunks
        while chunk := await file.read(1024):
            await f.write(chunk)

    # Get request ID from middleware (if set)
    request_id = getattr(request.state, "request_id", "-")

    # Response with file details
    headers = {
        "Content-Type": file.content_type,
        "Content-Disposition": f'inline; filename="{filename}"',
        "X-Request-ID": request_id
    }
    return Response(content=contents, headers=headers, media_type=file.content_type)