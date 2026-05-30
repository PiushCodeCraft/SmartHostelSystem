"""
encode_faces.py - Encodes face images from the dataset folder
and saves them to encodings/encodings.pkl

Run this script whenever you add new students:
    python recognition/encode_faces.py
"""

import face_recognition
import os
import pickle
import numpy as np
from PIL import Image
from tqdm import tqdm

# ── Paths ─────────────────────────────────────────────────────────────────────

DATASET_PATH   = "dataset"
ENCODINGS_PATH = "encodings/encodings.pkl"

os.makedirs("encodings", exist_ok=True)

# ── Encode Faces ──────────────────────────────────────────────────────────────

def encode_faces():
    known_encodings = []
    known_names     = []

    student_folders = [
        f for f in os.listdir(DATASET_PATH)
        if os.path.isdir(os.path.join(DATASET_PATH, f))
    ]

    if not student_folders:
        print("[!] No student folders found in dataset/")
        return

    print(f"[+] Found {len(student_folders)} student(s). Starting encoding...\n")

    for student_id in tqdm(student_folders, desc="Encoding"):
        folder_path = os.path.join(DATASET_PATH, student_id)

        image_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        if not image_files:
            print(f"    [!] No images found for {student_id}, skipping.")
            continue

        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)

            try:
                # Open with PIL, convert to RGB, ensure uint8
                pil_image = Image.open(image_path).convert("RGB")
                image     = np.array(pil_image, dtype=np.uint8)

                # Use cnn model for better detection, fallback to hog
                try:
                    locations = face_recognition.face_locations(image, model="cnn")
                except Exception:
                    locations = face_recognition.face_locations(image, model="hog")

                if len(locations) == 0:
                    # Try with upsampling if no face found
                    locations = face_recognition.face_locations(
                        image,
                        number_of_times_to_upsample=2,
                        model="hog"
                    )

                if len(locations) == 0:
                    print(f"    [!] No face detected in {image_path}, skipping.")
                    continue

                encodings = face_recognition.face_encodings(
                    image,
                    known_face_locations=locations,
                    num_jitters=2
                )

                if len(encodings) == 0:
                    print(f"    [!] Could not encode face in {image_path}, skipping.")
                    continue

                known_encodings.append(encodings[0])
                known_names.append(student_id)
                print(f"    [✓] Encoded {image_file} for {student_id}")

            except Exception as e:
                print(f"    [!] Error processing {image_path}: {e}")

    if not known_encodings:
        print("\n[!] No valid face encodings generated.")
        return

    data = {
        "encodings": known_encodings,
        "names":     known_names
    }

    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump(data, f)

    print(f"\n[✓] Encoded {len(known_encodings)} face(s) for {len(set(known_names))} student(s).")
    print(f"[✓] Saved to {ENCODINGS_PATH}")


if __name__ == "__main__":
    encode_faces()