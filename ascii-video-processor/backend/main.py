from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
from service import VideoProcessor
from ascii_config import RENDERING_CONFIG, RenderingConfig
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/process-video")
async def process_video(
    file: UploadFile = File(...),
    config: str = Form(...)
):
    config_dict = json.loads(config)
    config_model = RenderingConfig(**config_dict)

    # Save uploaded file
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
   
    # Process video
        processor = VideoProcessor(f"uploads/{file.filename}", config_model)
    output_path = processor.process_video()
    
    return FileResponse(output_path, media_type='video/mp4', filename=output_path.split('/')[-1])