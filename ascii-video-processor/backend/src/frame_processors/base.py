from abc import ABC, abstractmethod
import numpy as np

class FrameProcessor(ABC):
    @abstractmethod
    async def process(self, frame, context):
        """Process a single frame"""
        pass