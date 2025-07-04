import cv2
import os
import numpy as np
from PIL import Image

# Paths
dataset_path = 'dataset'
trainer_path = 'trainer'
model_file = os.path.join(trainer_path, 'trainer.yml')

# Create folder for model if not exist
os.makedirs(trainer_path, exist_ok=True)

# LBPH Recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Prepare training data
def get_images_and_labels(dataset_path):
    face_samples = []
    ids = []

    for folder_name in os.listdir(dataset_path):
        student_folder = os.path.join(dataset_path, folder_name)

        # Extract numeric ID from folder name (format: 101_Arun)
        student_id = int(folder_name.split('_')[0])

        for image_file in os.listdir(student_folder):
            image_path = os.path.join(student_folder, image_file)
            pil_img = Image.open(image_path).convert('L')  # Grayscale
            img_numpy = np.array(pil_img, 'uint8')

            faces = face_cascade.detectMultiScale(img_numpy)

            for (x, y, w, h) in faces:
                face_samples.append(img_numpy[y:y+h, x:x+w])
                ids.append(student_id)

    return face_samples, ids

print("[INFO] Training faces... Please wait.")
faces, ids = get_images_and_labels(dataset_path)

recognizer.train(faces, np.array(ids))
recognizer.save(model_file)

print("Training images:", len(faces))
print("Unique IDs:", len(set(ids)))
print(f"[INFO] {len(np.unique(ids))} students trained. Model saved to {model_file}")
print("[INFO] Training complete.")