from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
from service import VideoProcessor
from ascii_config import RENDERING_CONFIG, RenderingConfig
import json
from font_manager import FontManager
import logging

# Add debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create necessary directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("fonts", exist_ok=True)
os.makedirs("output", exist_ok=True)

app = FastAPI()

font_manager = FontManager()

logger.debug("Setting up CORS middleware...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.debug("CORS middleware setup complete")

@app.get("/api/fonts")
async def get_fonts():
    return font_manager.list_fonts()

@app.post("/api/process-video")
async def process_video(
    file: UploadFile = File(...),
    config: str = Form(...)
):
    logger.debug(f"Received request with headers: {file.headers}")
    config_dict = json.loads(config)
    config_model = RenderingConfig(**config_dict)

    # Save uploaded file
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
   
    # Process video
    processor = VideoProcessor(f"uploads/{file.filename}", config_model)
    output_path = processor.process_video()
    
    return FileResponse(output_path, media_type='video/mp4', filename=output_path.split('/')[-1])