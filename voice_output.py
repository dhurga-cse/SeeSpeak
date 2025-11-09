import pyttsx3
import tkinter as tk

engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

def speak_text():
    text = entry.get()
    if text:
        engine.say(text)
        engine.runAndWait()

root = tk.Tk()
root.title("SeeSpeak - Voice Output Test")
root.geometry("400x200")
root.configure(bg="#E6F3FF")

tk.Label(root, text="Enter text to speak:", bg="#E6F3FF", fg="#003366", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

tk.Button(root, text="Speak", command=speak_text, bg="#007BFF", fg="white", font=("Arial", 12), width=15).pack(pady=10)
tk.Button(root, text="Quit", command=root.destroy, bg="#FF6347", fg="white", font=("Arial", 12), width=15).pack(pady=5)

root.mainloop()
