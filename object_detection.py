from ultralytics import YOLO
import cv2

_model = YOLO("yolov8n.pt") 

def detect_objects(frame, conf=0.35):
    results = _model.predict(source=frame, conf=conf, verbose=False)[0]
    found = []
    for box in results.boxes:
        cls_id = int(box.cls[0])
        name = results.names[cls_id]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        score = float(box.conf[0])

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 190, 0), 2)
        cv2.putText(frame, f"{name} {score:.2f}",
                    (x1, max(y1 - 5, 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 190, 0), 1)

        found.append((name, (x1, y1, x2, y2), score))
    return found
