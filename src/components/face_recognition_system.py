import os
import cv2
import numpy as np
from tkinter import messagebox


class FaceRecognitionSystem:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.data_dir = "captured_images"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def capture_images(self, student_id):
        cap = cv2.VideoCapture(0)
        count = 0
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for x, y, w, h in faces:
                count += 1
                face = gray[y : y + h, x : x + w]
                file_name = f"{self.data_dir}/{student_id}_{count}.jpg"
                cv2.imwrite(file_name, face)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(
                    frame,
                    str(count),
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 0, 0),
                    2,
                )
            cv2.imshow("Capturing Images", frame)
            if cv2.waitKey(1) & 0xFF == ord("q") or count >= 30:
                break
        cap.release()
        cv2.destroyAllWindows()

    def recognize_student(self):
        labels = []
        faces = []
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith("jpg"):
                    path = os.path.join(root, file)
                    label = int(file.split("_")[0])
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    faces.append(img)
                    labels.append(label)
        if len(labels) == 0:
            messagebox.showwarning(
                "Warning",
                "No hay imágenes para entrenar el sistema de reconocimiento facial.",
            )
            return
        self.recognizer.train(faces, np.array(labels))
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for x, y, w, h in faces:
                face = gray[y : y + h, x : x + w]
                label, confidence = self.recognizer.predict(face)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(
                    frame,
                    f"ID: {label}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 0, 0),
                    2,
                )
            cv2.imshow("Reconociendo Estudiantes", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()
