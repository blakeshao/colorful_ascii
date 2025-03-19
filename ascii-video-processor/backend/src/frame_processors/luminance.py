from frame_processors.base import FrameProcessor
import cv2

class LuminanceFrameProcessor(FrameProcessor):
    def process(self, frame, context):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_gray = cv2.resize(gray, (context['columns'], context['rows']))
        normalized = resized_gray / 255.0
        return normalized