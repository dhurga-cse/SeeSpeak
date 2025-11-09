import torch
import cv2
import pyttsx3
import threading
from collections import Counter
import tkinter as tk
from tkinter import messagebox


engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)

camera_index = 0
cap = None
running = False
last_detected = []

def speak(text):
    """Speaks the detected object names."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

def detect_objects():
    """Runs YOLOv5 model continuously on webcam feed."""
    global running, cap, last_detected

    while running:
        ret, frame = cap.read()
        if not ret:
            print(" Camera frame not available.")
            break

        results = model(frame)
        labels = results.xyxyn[0][:, -1].cpu().numpy()
        names = results.names
        detected_objects = [names[int(i)] for i in labels]

        if detected_objects:
            unique_objects = list(set(detected_objects))
            if Counter(unique_objects) != Counter(last_detected):
                print("Detected:", ", ".join(unique_objects))
                threading.Thread(target=speak, args=("Detected " + ", ".join(unique_objects),), daemon=True).start()
                last_detected = unique_objects

        cv2.imshow("SeeSpeak - Object Detection", results.render()[0])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_detection()

    stop_detection()


def start_detection():
    """Start webcam and object detection."""
    global running, cap, camera_index
    if not running:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            messagebox.showerror("Camera Error", "Camera not accessible!")
            return

        running = True
        threading.Thread(target=detect_objects, daemon=True).start()
        messagebox.showinfo("Detection Started", "Object detection started. Press 'q' to stop.")


def stop_detection():
    """Stop webcam and close OpenCV window."""
    global running, cap
    running = False
    if cap:
        cap.release()
        cap = None
    cv2.destroyAllWindows()


def switch_camera():
    """Toggle between front and back cameras."""
    global camera_index, running
    if running:
        stop_detection()
    camera_index = 1 if camera_index == 0 else 0
    messagebox.showinfo("Camera Switched", f"Switched to {'Back' if camera_index == 1 else 'Front'} Camera")


root = tk.Tk()
root.title(" SeeSpeak - Object Detection with Voice Output")
root.geometry("420x250")
root.configure(bg="#E6F3FF")

tk.Label(
    root,
    text="👓 SeeSpeak - Object Detection with Voice Output",
    bg="#E6F3FF",
    fg="#003366",
    font=("Arial", 14, "bold"),
).pack(pady=15)

tk.Button(
    root,
    text=" Start Detection",
    command=start_detection,
    bg="#00BFFF",
    fg="white",
    font=("Arial", 12, "bold"),
    width=20
).pack(pady=5)

tk.Button(
    root,
    text="Switch Camera",
    command=switch_camera,
    bg="#32CD32",
    fg="white",
    font=("Arial", 12, "bold"),
    width=20
).pack(pady=5)

tk.Button(
    root,
    text=" Quit",
    command=lambda: [stop_detection(), root.destroy()],
    bg="#FF6347",
    fg="white",
    font=("Arial", 12, "bold"),
    width=20
).pack(pady=10)


root.mainloop()
