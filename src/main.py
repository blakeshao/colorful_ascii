import cv2
from ascii_config import ASCII_COLUMNS
from PIL import Image, ImageDraw, ImageFont

class VideoProcessor:
    def __init__(self, video_path, font, font_size):
        self.video_path = video_path
        self.columns = ASCII_COLUMNS
        self.aspect_ratio = 0.0
        self.rows = 0
        self.fps = 0
        self.prep_video()   # Populate previous variables
        # Determine output dimensions from font size
        self.font = ImageFont.truetype(font, font_size) if font.endswith(('.ttf', '.otf')) else ImageFont.load_default()
        self.font_size = font_size
        self.char_width, self.char_height = self.get_font_dimensions('X')
        self.output_width = self.columns * self.char_width
        self.output_height = self.rows * self.char_height


    def prep_video(self):
        cap = cv2.VideoCapture(self.video_path)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.aspect_ratio = cap.get(cv2.CAP_PROP_ASPECT_RATIO)
        self.rows = int(self.columns * self.aspect_ratio)

    def process_video(self):
        cap = cv2.VideoCapture(self.video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("frame", frame)


    def ascii_art(frame):
        pass


def main():
    video_processor = VideoProcessor("video.mp4", "Arial")
    video_processor.process_video()
