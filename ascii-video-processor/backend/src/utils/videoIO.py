import cv2
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class VideoIO:
    @staticmethod
    def read_video(video_path):
        frames = []
        cap = cv2.VideoCapture(video_path)
        cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame) 
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyWindow('Video')
        return frames

    @staticmethod
    def write_video(frames, output_path, fps, dimensions):
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        out = cv2.VideoWriter(output_path, fourcc, fps, dimensions)
        cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
        for frame in frames:
            out.write(frame)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        out.release()
        cv2.destroyWindow('Video')

  