import face_recognition
import cv2
import os
import pickle
import sys

if len(sys.argv) != 3:
    print("❌ Usage: python register.py <register_number> <name>")
    exit()

register_number = sys.argv[1]
full_name = sys.argv[2]
folder_name = f"{register_number}_{full_name}".replace(" ", "_")

# Create dataset folder
save_path = os.path.join("dataset", folder_name)
os.makedirs(save_path, exist_ok=True)

cam = cv2.VideoCapture(0)
print("\n[INFO] Press 'Q' to quit early. Capturing 10 images...")

img_count = 0
max_images = 10
encodings_list = []

while True:
    ret, frame = cam.read()
    if not ret:
        print("❌ [ERROR] Could not access camera.")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)

    for (top, right, bottom, left) in boxes:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow("Registering Face", frame)

    if len(boxes) == 1:
        encoding = face_recognition.face_encodings(rgb, boxes)[0]
        encodings_list.append(encoding)

        img_filename = os.path.join(save_path, f"face_{img_count+1}.jpg")
        cv2.imwrite(img_filename, frame)
        img_count += 1
        print(f"[INFO] Captured image {img_count}/{max_images}")

    if img_count >= max_images:
        print("✅ Done capturing.")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save encodings
if encodings_list:
    if os.path.exists("encodings.pkl"):
        with open("encodings.pkl", "rb") as f:
            data = pickle.load(f)
    else:
        data = {"encodings": [], "ids": [], "names": []}

    for encoding in encodings_list:
        data["encodings"].append(encoding)
        data["ids"].append(register_number)
        data["names"].append(full_name)

    with open("encodings.pkl", "wb") as f:
        pickle.dump(data, f)

    print(f"\n✅ Face encodings saved for {full_name} ({register_number})")

cam.release()
cv2.destroyAllWindows()
