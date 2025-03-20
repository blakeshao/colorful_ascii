import cv2

def luminance_process(frame, context):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_gray = cv2.resize(gray, (context['columns'], context['rows']))
    # Apply min-max normalization: (x - min) / (max - min)
    min_val = resized_gray.min()
    max_val = resized_gray.max()
    normalized = (resized_gray - min_val) / (max_val - min_val + 1e-8)  # Add small epsilon to prevent division by zero
    return normalized