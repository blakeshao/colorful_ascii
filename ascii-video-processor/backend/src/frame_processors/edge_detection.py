import cv2
import numpy as np

@staticmethod
def edge_detection_process(frame, context):
    # Get parameters from context or use defaults
    sigma = context.get('blur_sigma', 1.0)
    kernel_size = context.get('kernel_size', 5)
    low_threshold = context.get('low_threshold', 50)
    high_threshold = context.get('high_threshold', 150)
    edge_method = context.get('edge_method', 'canny')
    
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Advanced noise reduction
    blurred = cv2.GaussianBlur(gray, (kernel_size, kernel_size), sigma)
    
    if edge_method == 'canny':
        # Canny edge detection with automatic threshold calculation
        median = np.median(blurred)
        low_threshold = int(max(0, (1.0 - sigma) * median))
        high_threshold = int(min(255, (1.0 + sigma) * median))
        edges = cv2.Canny(blurred, low_threshold, high_threshold)
    
    elif edge_method == 'sobel':
        # Sobel edge detection
        sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
        edges = np.sqrt(sobelx**2 + sobely**2)
        edges = np.uint8(edges / edges.max() * 255)
    
    else:  # Laplacian
        # Laplacian edge detection
        edges = cv2.Laplacian(blurred, cv2.CV_64F)
        edges = np.uint8(np.absolute(edges))
    
    # Adaptive thresholding for better edge preservation
    edges = cv2.adaptiveThreshold(
        edges,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )
    
    # Morphological operations to clean up edges
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # Normalize and threshold
    normalized = edges.astype(float) / 255.0
    threshold = context.get('edge_threshold', 0.1)
    normalized = np.where(normalized > threshold, 1.0, 0.0)
    
    # Resize to target dimensions
    resized = cv2.resize(normalized, (context['columns'], context['rows']))
    return resized