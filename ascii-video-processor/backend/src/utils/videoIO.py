import cv2
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class VideoIO:
    @staticmethod
    def read_video(video_path):
        frames = []
        cap = cv2.VideoCapture(video_path)
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
        finally:
            cap.release()
        return frames

    @staticmethod
    def read_video_in_batches(video_path, batch_size=30):
        cap = cv2.VideoCapture(video_path)
        try:
            while cap.isOpened():
                frames = []
                for _ in range(batch_size):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frames.append(frame)
                if frames:
                    yield frames
                if not ret:
                    break
        finally:
            cap.release()

    @staticmethod
    def write_video(frames, output_path, fps, dimensions):
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        out = cv2.VideoWriter(output_path, fourcc, fps, dimensions)
        try:
            for frame in frames:
                out.write(frame)
        finally:
            out.release()
  

  