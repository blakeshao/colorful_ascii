import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool
from math import floor
from video.schema import RenderingConfig
from video.ascii_config import RENDERING_CONFIG
from frame_processors.luminance import luminance_process
from frame_processors.edge_detection import edge_detection_process
from utils.videoIO import VideoIO
from pathlib import Path
from functools import partial
from tqdm import tqdm

def process_frame_static(frame, columns, rows, char_width, char_height, config, font_path, font_size):
        if font_path.endswith(('.ttf', '.otf')):
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
            
        # Process frame based on rendering method
        context = {'columns': columns, 'rows': rows}
        
        if config['rendering_method'] == "LUMINANCE":
            processed_frame = luminance_process(frame, context)
        else:  # EDGE_DETECTION
            processed_frame = edge_detection_process(frame, context)
        
        # Create ASCII representation
        ascii = np.full((rows, columns), config['characters'][0]['char'])
        colors = np.full((rows, columns, 3), config['characters'][0]['color'])
        
        for char_config in config['characters']:
            mask = (processed_frame >= char_config['threshold'][0]) & (processed_frame < char_config['threshold'][1])
            ascii[mask] = char_config['char']
            colors[mask] = np.array(char_config['color'])
        
        # Render ASCII frame
        img = Image.new("RGB", (columns * char_width, rows * char_height), config['background_color'])
        draw = ImageDraw.Draw(img)
        
        for y_idx, row in enumerate(ascii):
            y = y_idx * char_height
            for x_idx, char in enumerate(row):
                x = x_idx * char_width
                draw.text((x, y), char, fill=tuple(colors[y_idx, x_idx]), font=font)
        
        frame_out = np.array(img)
        return cv2.cvtColor(frame_out, cv2.COLOR_RGB2BGR)

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
       


    def _setup_font(self):
        print("font_path: ", self.config.font_path)
        if self.config.font_path.endswith(('.ttf', '.otf')):
            font = ImageFont.truetype(self.config.font_path, self.config.font_size)
        else:
            font = ImageFont.load_default()
        self.char_width, self.char_height = self._get_font_dimensions(font)

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

    def _get_font_dimensions(self, font):
        dummy_img = Image.new("RGB", (100, 100))
        draw = ImageDraw.Draw(dummy_img)
        # Get the bounding box of the text
        bbox = draw.textbbox((0, 0), "A", font=font)
        # bbox returns (left, top, right, bottom)
        char_width = (bbox[2] - bbox[0])
        char_height = (bbox[3] - bbox[1])
        return char_width, char_height
    
    def process_video(self):
        print(f"Processing video: {self.video_path}")
        output_path = self._get_output_path()
        
        # Read all frames first
        print("Reading video frames...")
        frames = VideoIO.read_video(self.video_path)
        print(f"Total frames to process: {len(frames)}")
        
        # Convert Pydantic models to dict and create a simplified config
        config_dict = {
            'rendering_method': self.config.rendering_method,
            'background_color': self.config.background_color,
            'characters': [
                {
                    'char': c.char,
                    'threshold': c.threshold,
                    'color': c.color
                } for c in self.config.characters
            ]
        }
        
        # Create processing context with serializable data only
        process_context = {
            'columns': self.columns,
            'rows': self.rows,
            'char_width': self.char_width,
            'char_height': self.char_height,
            'config': config_dict,
            'font_path': self.config.font_path,
            'font_size': self.config.font_size
        }
        
        # Use functools.partial with the static function
        frame_processor = partial(process_frame_static, **process_context)
        
        print("Processing frames in parallel...")
        with Pool(processes=cpu_count()) as pool:
            processed_frames = list(tqdm(
                pool.imap(frame_processor, frames),
                total=len(frames),
                desc="Processing frames"
            ))
        
        print(f"Writing {len(processed_frames)} processed frames...")
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

