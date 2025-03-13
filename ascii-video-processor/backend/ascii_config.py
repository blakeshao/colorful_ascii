from schema import ASCII_Character, RenderingConfig


ASCII_CHARS = [
    ASCII_Character(char=".", threshold=(0, 0.1), color=(0, 0, 0)),
    ASCII_Character(char=":", threshold=(0.2, 0.3), color=(0, 0, 0)),
    ASCII_Character(char="0", threshold=(0.3, 0.4), color=(0, 0, 0)),
    ASCII_Character(char="+", threshold=(0.4, 0.5), color=(0, 0, 0)),
    ASCII_Character(char="*", threshold=(0.5, 1.0), color=(0, 0, 0)),
]


RENDERING_CONFIG = RenderingConfig(
    font_size=15,
    font_path="font/SF-Pro.ttf",
    background_color=(255, 255, 255),
    characters=ASCII_CHARS,
    original_color=False,
)







