import cv2
import os
import numpy as np
from PIL import Image

# Create LBPH Recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Path to Dataset
dataset_path = "dataset"

faces = []
ids = []

# Student ID Mapping
student_ids = {}

current_id = 0

# Loop Through Student Folders
for student_name in os.listdir(dataset_path):

    student_path = os.path.join(dataset_path, student_name)

    if not os.path.isdir(student_path):
        continue

    # Assign Numeric ID
    student_ids[current_id] = student_name

    # Loop Through Images
    for image_name in os.listdir(student_path):

        image_path = os.path.join(student_path, image_name)

        # Open Image
        img = Image.open(image_path).convert('L')

        image_np = np.array(img, 'uint8')

        faces.append(image_np)

        ids.append(current_id)

    current_id += 1

# Train Recognizer
recognizer.train(faces, np.array(ids))

# Create trainer folder if missing
os.makedirs("trainer", exist_ok=True)

# Save Trained Model
recognizer.save("trainer/trainer.yml")

print("Model Trained Successfully")
print("Trainer File Saved")