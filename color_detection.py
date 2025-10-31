import cv2, numpy as np

_COLOR_RGB = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "gray": (128, 128, 128),
    "red": (255, 0, 0),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "cyan": (0, 255, 255),
    "blue": (0, 0, 255),
    "purple": (128, 0, 128),
    "brown": (150, 75, 0),
}

def dominant_color_name(frame, box_size=120):
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2
    x1, y1 = max(cx - box_size//2, 0), max(cy - box_size//2, 0)
    x2, y2 = min(cx + box_size//2, w), min(cy + box_size//2, h)
    roi = frame[y1:y2, x1:x2]
    if roi.size == 0:
        return None

    avg_bgr = roi.reshape(-1, 3).mean(axis=0)
    avg_rgb = avg_bgr[::-1]
    avg = np.array(avg_rgb)

    def dist(name): return np.linalg.norm(avg - np.array(_COLOR_RGB[name]))
    return min(_COLOR_RGB.keys(), key=dist)
