import cv2
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class VideoIO:
    @staticmethod
    def read_video(video_path):
        frames = []
        # Verify file exists
        if not Path(video_path).exists():
            raise FileNotFoundError(f"Video file not found at: {video_path}")
            
        # Get file size and check if it's empty
        file_size = Path(video_path).stat().st_size
        if file_size == 0:
            raise RuntimeError(f"Video file is empty at: {video_path}")
            
        cap = cv2.VideoCapture(str(video_path))  # Ensure path is string
        if not cap.isOpened():
            # Get more detailed information about the failure
            fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
            fourcc_str = ''.join([chr((fourcc_int >> 8 * i) & 0xFF) for i in range(4)])
            logger.error(f"Video properties - FourCC: {fourcc_str} ({fourcc_int})")
            logger.error(f"Video file size: {file_size} bytes")
            
            # Try opening with different backend APIs
            for api in [cv2.CAP_FFMPEG, cv2.CAP_GSTREAMER]:
                logger.info(f"Attempting to open video with API: {api}")
                cap = cv2.VideoCapture(str(video_path), api)
                if cap.isOpened():
                    break
            
            if not cap.isOpened():
                raise RuntimeError(
                    f"OpenCV failed to open video at: {video_path}. "
                    "Please ensure the video format is supported and required codecs are installed. "
                    "Supported formats include: MP4 (H.264), AVI, MOV."
                )

        try:
            # Log video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            logger.info(f"Video properties - FPS: {fps}, Frames: {frame_count}, Resolution: {width}x{height}")
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
        finally:
            cap.release()
            
        if not frames:
            raise RuntimeError(f"No frames were read from video at: {video_path}. The video might be corrupted or in an unsupported format.")
        return frames

    @staticmethod
    def read_video_in_batches(video_path, batch_size=30):
        # Similar checks as read_video
        if not Path(video_path).exists():
            raise FileNotFoundError(f"Video file not found at: {video_path}")
            
        file_size = Path(video_path).stat().st_size
        if file_size == 0:
            raise RuntimeError(f"Video file is empty at: {video_path}")
            
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            logger.error(f"Video properties - FourCC: {int(cap.get(cv2.CAP_PROP_FOURCC))}")
            logger.error(f"Video file size: {file_size} bytes")
            raise RuntimeError(f"OpenCV failed to open video at: {video_path}. Please ensure the video format is supported (e.g., MP4 with H.264 encoding).")
        
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
        # Try different codecs in order of preference
        codecs = ['avc1', 'mp4v', 'XVID']
        
        for codec in codecs:
            fourcc = cv2.VideoWriter_fourcc(*codec)
            out = cv2.VideoWriter(output_path, fourcc, fps, dimensions)
            
            if out.isOpened():
                try:
                    for frame in frames:
                        out.write(frame)
                    logger.info(f"Successfully wrote video using codec: {codec}")
                    return
                finally:
                    out.release()
            else:
                out.release()
                
        raise RuntimeError("Failed to initialize VideoWriter with any available codec")
  

  