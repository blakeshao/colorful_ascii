from pydantic import BaseModel
class ASCII_Character(BaseModel):
    char: str
    threshold: tuple[float, float]
    color: tuple[int, int, int]

class RenderingConfig(BaseModel):
    font_size: int
    font_path: str
    background_color: tuple[int, int, int]
    characters: list[ASCII_Character]



