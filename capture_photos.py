"""
capture_photos.py - Capture multiple photos for a student to improve recognition accuracy.
Usage: python capture_photos.py STU001
       python capture_photos.py STU001 20   (capture 20 photos)
"""

import cv2
import os
import sys
import time

student_id = sys.argv[1] if len(sys.argv) > 1 else input("Enter Student ID (e.g. STU001): ").strip()
count      = int(sys.argv[2]) if len(sys.argv) > 2 else 15

dataset_path = f"dataset/{student_id}"
os.makedirs(dataset_path, exist_ok=True)

# Find next image number
existing = len([f for f in os.listdir(dataset_path) if f.endswith(".jpg")])
print(f"\n[INFO] Capturing {count} photos for {student_id}")
print("[INFO] Press SPACE to capture | Press Q to quit\n")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

captured = 0

while captured < count:
    ret, frame = cap.read()
    if not ret:
        break

    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.putText(
        frame,
        f"Captured: {captured}/{count} | SPACE=capture Q=quit",
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
    )

    cv2.imshow(f"Capturing photos for {student_id}", frame)

    key = cv2.waitKey(1)

    if key == ord(' ') and len(faces) > 0:
        img_num  = existing + captured + 1
        img_path = f"{dataset_path}/{img_num}.jpg"
        cv2.imwrite(img_path, frame)
        captured += 1
        print(f"  [{captured}/{count}] Saved {img_path}")
        time.sleep(0.3)

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"\n[✓] Done! {captured} photos saved to {dataset_path}/")
print(f"[→] Now run: python recognition/encode_faces.py")
