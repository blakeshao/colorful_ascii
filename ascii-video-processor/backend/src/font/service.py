from pathlib import Path
from typing import Dict, List

class FontManager:
    def __init__(self):
        # Use an absolute path to the fonts directory at the project root
        self.fonts_dir = Path(__file__).parent.parent.parent / "fonts"
        self.fonts_dir.mkdir(exist_ok=True)
        self.available_fonts: Dict[str, Path] = self._scan_fonts()
        print(f"Fonts directory: {self.fonts_dir}")
        print(f"Available fonts: {self.available_fonts}")
    

    def _scan_fonts(self) -> Dict[str, Path]:
        fonts = {}
        for font_file in self.fonts_dir.glob("*.ttf"):
            # Use the filename (without extension) as both key and display name
            name = font_file.stem
            fonts[name] = self.fonts_dir / f"{name}.ttf"
        return fonts

    def get_font_path(self, font_name: str) -> str:
        # Strip any file extension if present
        font_name = font_name.replace('.ttf', '')
        
        # Strip any 'fonts/' prefix if present
        font_name = font_name.replace('fonts/', '')
        
        if font_name not in self.available_fonts:
            available = list(self.available_fonts.keys())
            raise ValueError(f"Font '{font_name}' not found. Available fonts: {available}")
            
        print(f"Font path: {self.available_fonts[font_name]}")
        return str(self.available_fonts[font_name])

    def list_fonts(self):
        return [{"name": font_name, "value": font_name} for font_name in self.available_fonts.keys()]