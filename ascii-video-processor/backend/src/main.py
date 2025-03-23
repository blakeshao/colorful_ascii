from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from video.router import router as video_router
from font.router import router as font_router
import uvicorn
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from gallery_videos.router import router as gallery_videos_router
# Add debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
# Create necessary directories
os.makedirs(BASE_DIR / "uploads", exist_ok=True)
os.makedirs(BASE_DIR / "fonts", exist_ok=True)
os.makedirs(BASE_DIR / "output", exist_ok=True)

app = FastAPI()


def clear_directory(directory: Path):
    logger.debug(f"Clearing directory: {directory}")
    if directory.exists():
        for file in directory.iterdir():
            if file.is_file():
                file.unlink()
                logger.debug(f"Deleted file: {file}")

clear_directory(BASE_DIR / "uploads")
clear_directory(BASE_DIR / "output")

logger.debug("Setting up CORS middleware...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://colorfulascii.vercel.app",
        "http://colorfulascii.vercel.app",
        "http://localhost:3000",
        "https://colorful-ascii.onrender.com"

    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.debug("CORS middleware setup complete")



app.include_router(video_router)
app.include_router(font_router)
app.include_router(gallery_videos_router)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)