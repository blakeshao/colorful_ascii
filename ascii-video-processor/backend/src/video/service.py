import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool
from math import floor
from video.schema import RenderingConfig
from video.ascii_config import RENDERING_CONFIG
from frame_processors.luminance import LuminanceFrameProcessor
from frame_processors.edge_detection import EdgeDetectionFrameProcessor
from utils.videoIO import VideoIO
from pathlib import Path
from functools import partial

class VideoProcessor:
    def __init__(self, video_path, rendering_config: RenderingConfig):
        self.config = rendering_config
        self._setup_font()
        self._setup_video(video_path)   
        print("columns: ", self.columns)
        print("rows: ", self.rows)
        print("width: ", self.width)
        print("height: ", self.height)
        print("fps: ", self.fps)
        self._setup_processor()


    def _setup_font(self):
        print("font_path: ", self.config.font_path)
        if self.config.font_path.endswith(('.ttf', '.otf')):
            self.font = ImageFont.truetype(self.config.font_path, self.config.font_size)
        else:
            self.font = ImageFont.load_default()
        self.char_width, self.char_height = self._get_font_dimensions()

    def _setup_video(self, video_path):
        self.video_path = video_path
        print(f"Attempting to open video at path: {video_path}")
        
        cap = cv2.VideoCapture(str(video_path))  # Ensure path is string
        if not cap.isOpened():
            raise ValueError(f"Failed to open video file at {video_path}")
            
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        if self.width == 0 or self.height == 0:
            cap.release()
            raise ValueError(f"Invalid video dimensions: {self.width}x{self.height}")
            
        self.columns = floor(self.width / self.char_width)
        self.rows = floor(self.height / self.char_height)
        self.output_width = int(self.columns * self.char_width)
        self.output_height = int(self.rows * self.char_height)
        cap.release()

    def _setup_processor(self):
        processors = {
            "LUMINANCE": LuminanceFrameProcessor(),
            "EDGE_DETECTION": EdgeDetectionFrameProcessor()
        }
        self.frame_processor = processors.get(self.config.rendering_method)
        if not self.frame_processor:
            raise ValueError(f"Unknown rendering method: {self.config.rendering_method}")

    def _get_font_dimensions(self):
        dummy_img = Image.new("RGB", (100, 100))
        draw = ImageDraw.Draw(dummy_img)
        # Get the bounding box of the text
        bbox = draw.textbbox((0, 0), "A", font=self.font)
        # bbox returns (left, top, right, bottom)
        char_width = (bbox[2] - bbox[0])
        char_height = (bbox[3] - bbox[1])
        return char_width, char_height
    
    def _process_chunk(self, args):
        chunk, ascii, draw, colors = args
        start_idx, end_idx = chunk
        for y_idx, row in enumerate(ascii[start_idx:end_idx], start_idx):
            y = y_idx * self.char_height
            for x_idx, char in enumerate(row):
                x = x_idx * self.char_width
                draw.text((x, y), char, fill=tuple(colors[y_idx, x_idx]), font=self.font)

    def create_ascii_frame(self, normalized_frame):
        ascii = np.full((self.rows, self.columns), self.config.characters[0].char)
        colors = np.full((self.rows, self.columns, 3), self.config.characters[0].color)
        
        for char_config in self.config.characters:
            mask = (normalized_frame >= char_config.threshold[0]) & (normalized_frame < char_config.threshold[1])
            ascii[mask] = char_config.char
            colors[mask] = np.array(char_config.color)
            
        return ascii, colors
    
    def _render_ascii_frame(self, ascii, colors):
        print("Rendering ascii frame...")
        img = Image.new("RGB", (self.output_width, self.output_height), self.config.background_color)
        draw = ImageDraw.Draw(img)
        
        chunk_size = max(1, self.rows // cpu_count())
        chunks = [(i, min(i + chunk_size, self.rows)) for i in range(0, self.rows, chunk_size)]
        chunk_args = [(chunk, ascii, draw, colors) for chunk in chunks]
        
        with ThreadPool(processes=cpu_count()) as pool:
            pool.map(self._process_chunk, chunk_args)
        
        frame_out = np.array(img)
        return cv2.cvtColor(frame_out, cv2.COLOR_RGB2BGR)
    
    def _process_frame(self, frame):
        """Process a single frame with the frame processor"""
        print("Processing frame...")
        context = {
            'columns': self.columns,
            'rows': self.rows
        }
        normalized_frame = self.frame_processor.process(frame, context)
        ascii, colors = self.create_ascii_frame(normalized_frame)
        frame_out = self._render_ascii_frame(ascii, colors)
        return frame_out

    def process_video(self):
        print(f"Processing video: {self.video_path}")
        output_path = self._get_output_path()
        
        frames = VideoIO.read_video(self.video_path)
    

        print("Processing frames in parallel...")
        with Pool(processes=cpu_count()) as pool:
            processed_frames = pool.map(self._process_frame, frames)
        # processed_frames = []
        # for frame in frames:
        #     processed_frames.append(self._process_frame(frame))
            
        print("Processed frames: ", len(processed_frames))
        VideoIO.write_video(processed_frames, output_path, self.fps, (self.output_width, self.output_height))
        return output_path

 
        
    def _get_output_path(self):
        BASE_DIR = Path(__file__).parent.parent.parent
        output_dir = BASE_DIR / "output"
        output_dir.mkdir(exist_ok=True)
        video_name = Path(self.video_path).stem
        return str(output_dir / f"{video_name}_font_size_{self.config.font_size}.mp4")

        

    # def _process_chunk(self, args):
    #     chunk, ascii, draw, colors = args
    #     start_idx, end_idx = chunk
    #     for y_idx, row in enumerate(ascii[start_idx:end_idx], start_idx):
    #         y = y_idx * self.char_height
    #         for x_idx, char in enumerate(row):
    #             x = x_idx * self.char_width
    #             draw.text((x, y), char, fill=tuple(colors[y_idx, x_idx]), font=self.font)

    # def process_frame(self, frame):
    #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #     resized_gray = cv2.resize(gray, (self.columns, self.rows))

    #     normalized = resized_gray / 255.0
    #     ascii = np.full((self.rows, self.columns), self.ascii_characters[0].char)
    #     if self.original_color:
    #         colors = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         colors = cv2.resize(colors, (self.columns, self.rows))
    #         colors = [tuple(pixel) for row in colors for pixel in row]
    #         colors = np.array(colors).reshape(self.rows, self.columns, 3)
    #     else:
    #         colors = np.full((self.rows, self.columns, 3), self.ascii_characters[0].color)

    #         for config in self.ascii_characters:
    #             mask = (normalized >= config.threshold[0]) & (normalized < config.threshold[1])
    #             ascii[mask] = config.char
    #             colors[mask] = np.array(config.color)

    #     # Create the output image
    #     img = Image.new("RGB", (self.output_width, self.output_height), self.background_color)
    #     draw = ImageDraw.Draw(img)

    #     chunk_size = max(1, self.rows // cpu_count())
    #     chunks = [(i, min(i + chunk_size, self.rows)) for i in range(0, self.rows, chunk_size)]
        
    #     chunk_args = [(chunk, ascii, draw, colors) for chunk in chunks]

    #     with ThreadPool(processes=cpu_count()) as pool:
    #         pool.map(self._process_chunk, chunk_args)
        
    #     frame_out = np.array(img)
    #     frame_out = cv2.cvtColor(frame_out, cv2.COLOR_RGB2BGR)
    #     return frame_out

    # def process_video(self):
    #     print(f"Processing video: {self.video_path}")
    #     cap = cv2.VideoCapture(self.video_path)
    #     fourcc = cv2.VideoWriter_fourcc(*'avc1')
    #     output_path = f"output/{self.video_path.split('/')[-1].split('.')[0]}_font_size_{self.font_size}.mp4"
    #     out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.output_width, self.output_height))

    #     frames = []
    #     while cap.isOpened():
    #         ret, frame = cap.read()
    #         if not ret:
    #             break
    #         frames.append(frame)
    #         # cv2.imshow("frame", frame)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break

    #     # Process frames in parallel
    #     with Pool(processes=cpu_count()) as pool:
    #         match self.rendering_method:
    #             case "LUMINANCE":
    #                 processed_frames = pool.map(self.process_frame_luminance, frames)
    #             case "EDGE_DETECTION":
    #                 processed_frames = pool.map(self.process_frame_edge_detection, frames)

    #     # Write processed frames
    #     for frame_out in processed_frames:
    #         print("frame_out: ", frame_out.shape)
    #         out.write(frame_out)
    #         # cv2.imshow("frame_out", frame_out)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break

    #     cap.release()
    #     out.release()
    #     cv2.destroyAllWindows()
    #     return output_path

   


def main():
    video_processor = VideoProcessor("video/boxing.mp4", RENDERING_CONFIG)
    video_processor.process_video()

if __name__ == "__main__":
    main()