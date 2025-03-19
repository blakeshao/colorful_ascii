from frame_processors.base import FrameProcessor
import cv2
import numpy as np

class EdgeDetectionFrameProcessor(FrameProcessor):
    def process(self, frame, context):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        normalized = cv2.normalize(gradient_magnitude, None, 0, 1, cv2.NORM_MINMAX)
        resized = cv2.resize(normalized, (context['columns'], context['rows']))
        return resized