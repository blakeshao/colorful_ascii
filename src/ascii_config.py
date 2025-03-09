from schema import ASCII_Character, RenderingConfig


ASCII_CHARS = [
    ASCII_Character(char=".", threshold=(0, 0.2), color=(255, 0, 0)),
    ASCII_Character(char=":", threshold=(0.2, 0.4), color=(0, 255, 0)),
    ASCII_Character(char="-", threshold=(0.4, 0.6), color=(0, 0, 255)),
    ASCII_Character(char="+", threshold=(0.6, 0.8), color=(255, 255, 0)),
    ASCII_Character(char="*", threshold=(0.8, 1.0), color=(0, 255, 255)),
]


RENDERING_CONFIG = RenderingConfig(
    font_size=20,
    font_path="font/SF-Pro.ttf",
    background_color=(255, 255, 255),
    characters=ASCII_CHARS
)







