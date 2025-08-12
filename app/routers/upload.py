from fastapi import APIRouter, File, UploadFile, Request, HTTPException, Response
import os

upload_router = APIRouter()
MAX_SIZE = 5 * 1024 * 1024

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
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Check file size
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file")
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    
    # Sanitize filename
    filename = sanitize_filename(file.filename)

    # Get request ID from middleware (if set)
    request_id = getattr(request.state, "request_id", "-")

    # Response with file details
    headers = {
        "Content-Type": file.content_type,
        "Content-Disposition": f'inline; filename="{filename}"',
        "X-Request-ID": request_id
    }
    return Response(content=contents, headers=headers, media_type=file.content_type)