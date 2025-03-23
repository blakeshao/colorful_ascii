from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import FileResponse
import json
from video.service import VideoProcessor
from video.schema import RenderingConfig
import shutil
import logging
import os
from pathlib import Path
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")

BASE_DIR = Path(__file__).parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.gif'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

@router.post("/process-video")
async def process_video(
    file: UploadFile = File(...),
    config: str = Form(...)
):
    try:
        # Validate file size
        if file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
            
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Invalid file type")

        # Generate safe filename
        safe_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / safe_filename

        # Ensure upload directory exists
        UPLOAD_DIR.mkdir(exist_ok=True)

        # Parse and validate config
        try:
            config_dict = json.loads(config)
            config_model = RenderingConfig(**config_dict)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON configuration")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Save uploaded file
        with file.file as source, open(file_path, "wb") as buffer:
            shutil.copyfileobj(source, buffer)
        
            # Process video
            print("Processing video...")
            processor = VideoProcessor(str(file_path), config_model)
            output_path = processor.process_video()
            
            # Return the processed video
            return FileResponse(
                output_path,
                media_type='video/mp4',
                filename=Path(output_path).name,
                headers={
                    "Accept-Ranges": "bytes",
                    "Content-Disposition": f'inline; filename="{Path(output_path).name}"'
                }
            )

            
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")