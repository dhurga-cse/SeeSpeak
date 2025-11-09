import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

def run_script(script_name):
    """Run a Python file in a separate process."""
    script_path = os.path.join(os.getcwd(), script_name)
    if not os.path.exists(script_path):
        messagebox.showerror("Error", f"{script_name} not found!")
        return
    subprocess.Popen([sys.executable, script_path])

def open_object_detection():
    run_script("object_detection_gui.py")

def open_text_recognition():
    run_script("text_recognition.py")

def open_voice_output_test():
    run_script("voice_output.py")

def exit_app():
    root.destroy()


root = tk.Tk()
root.title(" SeeSpeak - AI Vision Assistant")
root.geometry("450x300")
root.configure(bg="#E6F3FF")

tk.Label(
    root,
    text=" SeeSpeak - AI Vision Assistant",
    bg="#E6F3FF",
    fg="#003366",
    font=("Arial", 16, "bold"),
).pack(pady=20)

tk.Button(
    root,
    text=" Object Detection",
    command=open_object_detection,
    bg="#007BFF",
    fg="white",
    font=("Arial", 12, "bold"),
    width=25
).pack(pady=8)

tk.Button(
    root,
    text="Text Recognition",
    command=open_text_recognition,
    bg="#32CD32",
    fg="white",
    font=("Arial", 12, "bold"),
    width=25
).pack(pady=8)

tk.Button(
    root,
    text="Voice Output Test",
    command=open_voice_output_test,
    bg="#FFA500",
    fg="white",
    font=("Arial", 12, "bold"),
    width=25
).pack(pady=8)

tk.Button(
    root,
    text=" Quit",
    command=exit_app,
    bg="#FF6347",
    fg="white",
    font=("Arial", 12, "bold"),
    width=25
).pack(pady=10)

root.mainloop()
