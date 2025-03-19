from fastapi import APIRouter
from font.service import FontManager

router = APIRouter(prefix="/api")

font_manager = FontManager()

@router.get("/fonts")
async def get_fonts():
    print("Getting fonts...")
    return font_manager.list_fonts()