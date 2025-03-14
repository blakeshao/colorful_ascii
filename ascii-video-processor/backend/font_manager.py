from pathlib import Path
from typing import Dict, List

class FontManager:
    def __init__(self):
        self.fonts_dir = Path(__file__).parent / "fonts"
        self.fonts_dir.mkdir(exist_ok=True)
        self.available_fonts: Dict[str, Path] = self._scan_fonts()

    def _scan_fonts(self) -> Dict[str, Path]:
        fonts = {}
        for font_file in self.fonts_dir.glob("*.ttf"):
            # Store with a friendly name (without extension) as key
            friendly_name = font_file.stem.replace("-", " ")
            fonts[friendly_name] = font_file
        return fonts

    def get_font_path(self, font_name: str) -> str:
        return str(self.available_fonts[font_name])

    def list_fonts(self) -> List[dict]:
        return [
            {"name": name, "value": str(path.name)}
            for name, path in self.available_fonts.items()
        ]