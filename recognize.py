import cv2
import numpy as np
import os
import csv
from datetime import datetime

# Load recognizer and face detector
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/trainer.yml")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load student data
students = {}
with open("students.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # skip header
    for row in reader:
        students[int(row[0])] = row[1]

# Create attendance folder if not exists
os.makedirs("attendance", exist_ok=True)

# Daily attendance file
date_today = datetime.now().strftime("%Y-%m-%d")
filename = f"attendance/Attendance-{date_today}.csv"

# Keep track of already marked IDs
marked_ids = set()

# Create CSV file if not exists
if not os.path.exists(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Date", "Time"])

# Start webcam
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # ← DirectShow backend (Windows safe)


print("[INFO] Starting recognition. Press Q to quit.")
while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        id_, confidence = recognizer.predict(face)

        if confidence < 60:
            name = students.get(id_, "Unknown")

            # Mark attendance only once
            if id_ not in marked_ids:
                now = datetime.now()
                with open(filename, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([id_, name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")])
                marked_ids.add(id_)
                print(f"[INFO] Attendance marked for {name}")

            label = f"{name} (Conf: {round(confidence, 2)})"

            color = (0, 255, 0)
        else:
            label = "Unknown"
            color = (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.imshow("Face Recognition Attendance System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
print("[INFO] Recognition stopped.")