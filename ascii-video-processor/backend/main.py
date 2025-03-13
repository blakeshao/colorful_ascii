from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
from service import VideoProcessor
from ascii_config import RENDERING_CONFIG

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/process-video")
async def process_video(file: UploadFile = File(...)):
    # Save uploaded file
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process video
    processor = VideoProcessor(f"uploads/{file.filename}", RENDERING_CONFIG)
    output_path = processor.process_video()
    
    return FileResponse(output_path)