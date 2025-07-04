import face_recognition
import csv 
import cv2
import os
import pickle
from datetime import datetime

# Load known encodings
if not os.path.exists("encodings.pkl"):
    print("❌ No encodings found. Please register at least one student.")
    exit()

with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["names"]
known_ids = data["ids"]

# Prepare attendance log
attendance_file = "attendance.csv"
if not os.path.exists(attendance_file):
    with open(attendance_file, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["register_number", "name", "Time"])
        writer.writeheader()

# Track today's date
today_str = datetime.now().strftime("%Y-%m-%d")
marked = set()

# Load already marked today
if os.path.exists(attendance_file):
    with open(attendance_file, "r", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Time"].startswith(today_str):
                marked.add(row["register_number"])

cam = cv2.VideoCapture(0)
print("[INFO] Starting face recognition. Press 'Q' to quit.")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding, (top, right, bottom, left) in zip(encodings, boxes):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        name = "Unknown"
        reg_no = ""

        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]
            reg_no = known_ids[match_index]

            if reg_no not in marked:
                marked.add(reg_no)
                with open(attendance_file, "a", newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=["register_number", "name", "Time"])
                    writer.writerow({
                        "register_number": reg_no,
                        "name": name,
                        "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                print(f"✅ Marked Present: {name} ({reg_no})")
            else:
                print(f"[ℹ️] Already marked today for {name} ({reg_no})")

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Face Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
print("[INFO] Attendance session ended.")
