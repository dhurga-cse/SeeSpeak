import cv2
import pytesseract
import pyttsx3
import tkinter as tk
from tkinter import messagebox



engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_text():
    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Instructions", "Press 's' to capture image and detect text, 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Text Recognition - Press S to Capture", frame)

        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite("captured_text.jpg", frame)
            text = pytesseract.image_to_string(frame)
            print(" Detected Text:", text)
            if text.strip():
                speak("The text says: " + text)
            else:
                speak("No readable text found.")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

root = tk.Tk()
root.title(" SeeSpeak - Text Recognition")
root.geometry("400x200")
root.configure(bg="#E6F3FF")

tk.Label(
    root,
    text=" SeeSpeak - Text Recognition",
    bg="#E6F3FF",
    fg="#003366",
    font=("Arial", 14, "bold"),
).pack(pady=15)

tk.Button(
    root,
    text="Start Text Recognition",
    command=recognize_text,
    bg="#32CD32",
    fg="white",
    font=("Arial", 12),
    width=20
).pack(pady=10)

tk.Button(
    root,
    text="Quit",
    command=root.destroy,
    bg="#FF6347",
    fg="white",
    font=("Arial", 12),
    width=20
).pack(pady=10)

root.mainloop()
