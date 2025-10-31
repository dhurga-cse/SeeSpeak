import face_recognition
import cv2
import os

def load_known_faces(folder_path='known_faces'):
    known_encodings = []
    known_names = []

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f" Folder '{folder_path}' created. Add face images inside it.")
        return known_encodings, known_names

    for file in os.listdir(folder_path):
        img_path = os.path.join(folder_path, file)
        try:
            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(file)[0])
        except Exception as e:
            print(f" Skipping {file}: {e}")

    return known_encodings, known_names

def recognize_faces(frame, known_encodings, known_names):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        matches = face_recognition.compare_faces(known_encodings, encoding)
        if True in matches:
            index = matches.index(True)
            name = known_names[index]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 128, 255), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 128, 255), 2)

    return frame
