from fastapi import APIRouter, HTTPException
from pathlib import Path
from fastapi.responses import FileResponse
router = APIRouter(prefix="/api")

BASE_DIR = Path(__file__).parent.parent.parent


@router.get("/gallery_videos")
async def get_gallery_videos():
    print("BASE_DIR", BASE_DIR)
    gallery_dir = BASE_DIR / "gallery_videos"
    if not gallery_dir.exists():
        gallery_dir.mkdir(exist_ok=True)
        
    videos = []
    for video in gallery_dir.glob("*.mp4"):
        print("video", video)
        videos.append({
            "url": f"/api/gallery_videos/{video.name}",
            "filename": video.name
        })
    return videos

@router.get("/gallery_videos/{filename}")
async def get_video(filename: str):
    video_path = BASE_DIR / "gallery_videos" / filename
    print("video_path", video_path)
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(
        video_path,
        media_type='video/mp4',
        filename=filename
    )