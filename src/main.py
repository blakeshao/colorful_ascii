import cv2
from ascii_config import ASCII_CHARS
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool
from math import floor

class VideoProcessor:
    def __init__(self, video_path, font_path, font_size=20, background_color=(0, 0, 0)):
        # Determine output dimensions from font size
        self.font = ImageFont.truetype(font_path, font_size) if font_path.endswith(('.ttf', '.otf')) else ImageFont.load_default()
        self.font_size = font_size
        self.char_width, self.char_height = self._get_font_dimensions()
        print("char_width: ", self.char_width)
        print("char_height: ", self.char_height)

        self.background_color = (0, 0, 0)

        self.video_path = video_path
        self.columns = 0
        self.rows = 0
        self.width = 0
        self.height = 0
        self.fps = 0
        self._prep_video()   # Populate previous variables
        print("columns: ", self.columns)
        print("rows: ", self.rows)
        print("width: ", self.width)
        print("height: ", self.height)
        print("fps: ", self.fps)


        self.output_width = int(self.columns * self.char_width)
        self.output_height = int(self.rows * self.char_height)

        print("output_width: ", self.output_width)
        print("output_height: ", self.output_height)





    def _prep_video(self):
        cap = cv2.VideoCapture(self.video_path)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.columns = floor(self.width / self.char_width)
        self.rows = floor(self.height / self.char_height)

    def _get_font_dimensions(self):
        dummy_img = Image.new("RGB", (100, 100))
        draw = ImageDraw.Draw(dummy_img)
        # Get the bounding box of the text
        bbox = draw.textbbox((0, 0), "A", font=self.font)
        # bbox returns (left, top, right, bottom)
        char_width = (bbox[2] - bbox[0])*1.25
        char_height = (bbox[3] - bbox[1])*1.25
        return char_width, char_height
    
    def _process_chunk(self, args):
        chunk, ascii, draw = args
        start_idx, end_idx = chunk
        for y_idx, row in enumerate(ascii[start_idx:end_idx], start_idx):
            y = y_idx * self.char_height
            for x_idx, char in enumerate(row):
                x = x_idx * self.char_width
                draw.text((x, y), char, fill=(255, 255, 255), font=self.font)

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_gray = cv2.resize(gray, (self.columns, self.rows))

        normalized = (resized_gray / 255.0 * (len(ASCII_CHARS) - 1)).astype(int)
        ascii = np.array(list(ASCII_CHARS))[normalized]


        

        # Create the output image
        img = Image.new("RGB", (self.output_width, self.output_height), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw each line of ASCII text
        # y = 0
        # for line in ascii:
        #     # print("line: ", line)
        #     for i in range(len(line)):
        #         draw.text((i*self.char_width, y), line[i], fill=(255, 255, 255), font=self.font)
           
        #     y += self.char_height

        chunk_size = max(1, self.rows // cpu_count())
        chunks = [(i, min(i + chunk_size, self.rows)) for i in range(0, self.rows, chunk_size)]
        
        chunk_args = [(chunk, ascii, draw) for chunk in chunks]

        with ThreadPool(processes=cpu_count()) as pool:
            pool.map(self._process_chunk, chunk_args)
        
        frame_out = np.array(img)
        frame_out = cv2.cvtColor(frame_out, cv2.COLOR_RGB2BGR)
        return frame_out

    def process_video(self):
        print(f"Processing video: {self.video_path}")
        cap = cv2.VideoCapture(self.video_path)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter("output/ascii_output.mp4", fourcc, self.fps, (self.output_width, self.output_height))

        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Process frames in parallel
        with Pool(processes=cpu_count()) as pool:
            processed_frames = pool.map(self.process_frame, frames)

        # Write processed frames
        for frame_out in processed_frames:
            print("frame_out: ", frame_out.shape)
            out.write(frame_out)
            cv2.imshow("frame_out", frame_out)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

   


def main():
    video_processor = VideoProcessor("video/boxing.mp4", "font/SF-Pro.ttf", 20)
    video_processor.process_video()

if __name__ == "__main__":
    main()