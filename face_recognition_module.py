import face_recognition
import cv2
import os
import numpy as np

known_face_encodings = []
known_face_names = []

def load_known_faces():
    path = "known_faces"
    for file in os.listdir(path):
        img = face_recognition.load_image_file(f"{path}/{file}")
        encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(file)[0])

load_known_faces()

def recognize_faces(frame):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)
    recognized_faces = []

    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        recognized_faces.append(name)
    return recognized_faces
