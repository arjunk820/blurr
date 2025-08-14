# Face Blur API

A minimal FastAPI service that accepts image uploads, validates them, and echoes them back unchanged.
Built as the foundation for a face-blurring service using OpenCV.

## Getting Started

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```
uvicorn app.main:app --reload
```

```
# Health check
curl http://127.0.0.1:8000/health

# Upload an image
curl -X POST http://127.0.0.1:8000/upload/image \
  -F "file=@/path/to/photo.jpg" \
  -o echo.jpg
```

Modify the path of the image curl request as needed.