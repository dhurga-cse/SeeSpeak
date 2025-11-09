import cv2
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def detect_objects(frame):
    results = model(frame)
    detections = results.pandas().xyxy[0]
    detected_objects = detections['name'].tolist()

  
    for _, row in detections.iterrows():
        x1, y1, x2, y2, label = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax']), row['name']
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return detected_objects
