
import cv2
from collections import Counter

from face_recognition_module import load_known_faces, recognize_faces
from object_detection import detect_objects
from text_recognition import recognize_text
from color_detection import dominant_color_name
from voice_output import speak, set_voice, shutdown
from utils import beep

HELP_TEXT = [
    "SeeSpeak — Keys:",
    " q  = Quit",
    " f  = Front cam   |  b = Back cam (Iriun)",
    " o  = Toggle object announcements",
    " t  = Read center text (once)",
    " s  = Scene summary (top objects)",
    " c  = Say dominant color (center)",
    " g  = Set TARGET as object under crosshair (beep when centered)",
]

def draw_overlay(frame, camera_index, announce_objects, target):
    h, w = frame.shape[:2]
    cv2.drawMarker(frame, (w // 2, h // 2), (255, 255, 255), cv2.MARKER_CROSS, 20, 2)
    bar = f"Cam: {camera_index} | Announce: {'ON' if announce_objects else 'OFF'} | Target: {target or '-'}"
    cv2.rectangle(frame, (0, 0), (w, 28), (0, 0, 0), -1)
    cv2.putText(frame, bar, (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 255, 200), 1)

    y = 40
    for line in HELP_TEXT:
        cv2.putText(frame, line, (8, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1)
        y += 18

def pick_camera(prefer_index=1):
    """
    Prefer back cam (Iriun) at index 1 if available, otherwise 0.
    """
    for idx in [prefer_index, 0]:
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            return cap, idx
        cap.release()
    raise RuntimeError("No camera available")

def object_under_center(dets, w, h):
    """Return name of object whose box contains the center, else None."""
    cx, cy = w // 2, h // 2
    for name, (x1, y1, x2, y2), _ in dets:
        if x1 <= cx <= x2 and y1 <= cy <= y2:
            return name
    return None

def main():
    print("🔁 Loading known faces...")
    encodings, names = load_known_faces()

    cap, camera_index = pick_camera(prefer_index=1)  # try Iriun first
    announce_objects = True
    target = None

    set_voice(rate=175, volume=1.0)

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        h, w = frame.shape[:2]

        recognize_faces(frame, encodings, names)

        detections = detect_objects(frame, conf=0.35)  
        object_names = [n for (n, _, _) in detections]

        if announce_objects and object_names:
            count = Counter(object_names)
            top = ", ".join([f"{k} {v}" if v > 1 else k for k, v in count.most_common(5)])
            speak(f"Detected: {top}")

        if target:
            centered = object_under_center(detections, w, h)
            if centered and centered.lower() == target.lower():
                beep(1400, 120)

        draw_overlay(frame, camera_index, announce_objects, target)

        cv2.imshow("SeeSpeak", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        elif key == ord('f'): 
            cap.release()
            cap = cv2.VideoCapture(0)
            camera_index = 0
            speak("Front camera")

        elif key == ord('b'):  
            cap.release()
            cap = cv2.VideoCapture(1)  
            camera_index = 1
            speak("Back camera")

        elif key == ord('o'):  
            announce_objects = not announce_objects
            speak(f"Object announcements {'on' if announce_objects else 'off'}")

        elif key == ord('t'):  
            txt = recognize_text(frame, center_only=True)
            if txt:
                speak("Reading: " + txt)
                print("", txt)
            else:
                speak("No readable text")

        elif key == ord('s'):  
            if object_names:
                count = Counter(object_names)
                summary = ", ".join([f"{k} {v}" if v > 1 else k for k, v in count.most_common(5)])
                speak("Scene: " + summary)
                print(" Scene:", summary)
            else:
                speak("No objects")

        elif key == ord('c'):  
            col = dominant_color_name(frame)
            if col:
                speak(f"{col}")
                print(" Color:", col)
            else:
                speak("No color")

        elif key == ord('g'): 
            name = object_under_center(detections, w, h)
            if name:
                target = name
                speak(f"Target {name}")
                print("Target set:", name)
            else:
                target = None
                speak("No target")

    cap.release()
    cv2.destroyAllWindows()
    shutdown()

if __name__ == "__main__":
    main()
