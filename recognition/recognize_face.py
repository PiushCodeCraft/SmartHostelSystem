# import cv2
# import os
# import sys
# import time
# import pickle
# import numpy as np
# from datetime import datetime

# # ---------------------------------------------------
# # PROJECT ROOT PATH
# # ---------------------------------------------------

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import face_recognition
# from recognition.attendance_logic import mark_attendance
# from utils.logger import log_info, log_warn, log_error

# # ---------------------------------------------------
# # LOAD ENCODINGS
# # ---------------------------------------------------

# ENCODINGS_PATH = "encodings/encodings.pkl"

# if not os.path.exists(ENCODINGS_PATH):
#     log_error("face-recognition", "encodings.pkl not found. Run encode_faces.py first.")
#     exit()

# with open(ENCODINGS_PATH, "rb") as f:
#     data = pickle.load(f)

# known_encodings = data["encodings"]
# known_names     = data["names"]

# log_info("face-recognition", f"Loaded {len(known_names)} face encodings")

# # ---------------------------------------------------
# # SETTINGS
# # ---------------------------------------------------

# TOLERANCE        = 0.45   # Lower = stricter match (0.4-0.5 is best)
# CONFIRM_FRAMES   = 5      # Must be recognized N frames in a row before confirming
# COOLDOWN         = 10     # Seconds before re-marking attendance
# UNKNOWN_COOLDOWN = 15     # Seconds between saving unknown face images
# PROCESS_EVERY    = 2      # Process every Nth frame (for speed)

# # ---------------------------------------------------
# # STATE
# # ---------------------------------------------------

# last_recognized  = {}
# last_unknown_time = 0
# frame_count      = 0
# recognition_buffer = {}   # name -> consecutive frame count

# # ---------------------------------------------------
# # START CAMERA
# # ---------------------------------------------------

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# if not cap.isOpened():
#     log_error("camera", "Could not open webcam")
#     exit()

# # Set camera resolution for better accuracy
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# log_info("camera", "Webcam started")
# print("\n[INFO] Press ENTER to exit\n")

# # ---------------------------------------------------
# # MAIN LOOP
# # ---------------------------------------------------

# while True:

#     ret, frame = cap.read()

#     if not ret:
#         log_error("camera", "Failed to read frame")
#         break

#     frame_count += 1

#     # Only process every Nth frame for performance
#     if frame_count % PROCESS_EVERY == 0:

#         # Resize for faster processing
#         small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
#         rgb_frame   = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

#         # Detect face locations and encodings
#         face_locations = face_recognition.face_locations(rgb_frame, model="hog")
#         face_encodings = face_recognition.face_encodings(
#             rgb_frame,
#             face_locations,
#             num_jitters=2    # 2 jitters = better accuracy, still fast
#         )

#         current_names = []

#         for face_encoding in face_encodings:

#             # Compare with all known faces
#             distances = face_recognition.face_distance(known_encodings, face_encoding)

#             if len(distances) == 0:
#                 current_names.append("Unknown")
#                 continue

#             best_match_idx = np.argmin(distances)
#             best_distance  = distances[best_match_idx]

#             if best_distance < TOLERANCE:
#                 name = known_names[best_match_idx]
#             else:
#                 name = "Unknown"

#             current_names.append(name)

#             # ---------------------------------------------------
#             # CONFIRMATION BUFFER (N frames in a row)
#             # ---------------------------------------------------

#             if name != "Unknown":
#                 recognition_buffer[name] = recognition_buffer.get(name, 0) + 1

#                 if recognition_buffer[name] >= CONFIRM_FRAMES:
#                     current_time = time.time()

#                     if name not in last_recognized:
#                         last_recognized[name] = 0

#                     if (current_time - last_recognized[name]) > COOLDOWN:
#                         mark_attendance(name)
#                         last_recognized[name] = current_time
#                         recognition_buffer[name] = 0
#                         log_info("face-recognition", f"{name} marked successfully")
#             else:
#                 # Reset buffer for unknown
#                 recognition_buffer = {k: v for k, v in recognition_buffer.items() if k != "Unknown"}

#         # ---------------------------------------------------
#         # HANDLE UNKNOWN FACE SAVING
#         # ---------------------------------------------------

#         if "Unknown" in current_names:
#             current_time = time.time()
#             if (current_time - last_unknown_time) > UNKNOWN_COOLDOWN:
#                 os.makedirs("logs/unknown_faces", exist_ok=True)
#                 filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
#                 cv2.imwrite(f"logs/unknown_faces/{filename}", frame)
#                 last_unknown_time = current_time
#                 log_warn("face-recognition", f"Unknown face saved: {filename}")

#     # ---------------------------------------------------
#     # DRAW BOXES (scale back up from small_frame)
#     # ---------------------------------------------------

#     try:
#         for (top, right, bottom, left), name in zip(face_locations, current_names):
#             # Scale back up since we processed at 0.5x
#             top    *= 2
#             right  *= 2
#             bottom *= 2
#             left   *= 2

#             if name != "Unknown":
#                 color = (0, 255, 0)   # Green for known
#             else:
#                 color = (0, 0, 255)   # Red for unknown

#             cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
#             cv2.rectangle(frame, (left, bottom - 30), (right, bottom), color, cv2.FILLED)
#             cv2.putText(
#                 frame, name,
#                 (left + 6, bottom - 8),
#                 cv2.FONT_HERSHEY_DUPLEX,
#                 0.65, (255, 255, 255), 1
#             )
#     except Exception:
#         pass

#     cv2.imshow("Smart Hostel - Face Recognition  |  Press ENTER to exit", frame)

#     if cv2.waitKey(1) == 13:
#         break

# cap.release()
# cv2.destroyAllWindows()
# log_info("camera", "Face recognition stopped")
















import cv2
import os
import sys
import time
import pickle
import numpy as np
import streamlit as st
from datetime import datetime

# ---------------------------------------------------
# PROJECT ROOT PATH
# ---------------------------------------------------

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import face_recognition
from recognition.attendance_logic import mark_attendance
from utils.logger import log_info, log_warn, log_error

# ---------------------------------------------------
# LOAD ENCODINGS
# ---------------------------------------------------

ENCODINGS_PATH = "encodings/encodings.pkl"

if not os.path.exists(ENCODINGS_PATH):
    st.error("encodings.pkl not found. Run encode_faces.py first.")
    st.stop()

with open(ENCODINGS_PATH, "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names     = data["names"]

# ---------------------------------------------------
# SETTINGS (UNCHANGED)
# ---------------------------------------------------

TOLERANCE        = 0.45
CONFIRM_FRAMES   = 5
COOLDOWN         = 10
UNKNOWN_COOLDOWN = 15
PROCESS_EVERY    = 2
SCAN_DURATION    = 30  # NEW

# ---------------------------------------------------
# STREAMLIT PAGE
# ---------------------------------------------------

st.title("📷 Face Recognition")

scan = st.button("📷 Scan Face", type="primary")

# ---------------------------------------------------
# START SCAN
# ---------------------------------------------------

if scan:

    st.info("Camera opened. Looking for face...")

    last_recognized   = {}
    last_unknown_time = 0
    frame_count       = 0
    recognition_buffer = {}

    recognized = False
    timeout    = False

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        st.error("Could not open webcam")
        st.stop()

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    start_time = time.time()

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # ----------------------------------------
        # 30 SECOND TIMER
        # ----------------------------------------

        elapsed = time.time() - start_time

        if elapsed > SCAN_DURATION:
            timeout = True
            break

        frame_count += 1

        if frame_count % PROCESS_EVERY == 0:

            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_frame   = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_frame, model="hog")
            face_encodings = face_recognition.face_encodings(
                rgb_frame,
                face_locations,
                num_jitters=2
            )

            current_names = []

            for face_encoding in face_encodings:

                distances = face_recognition.face_distance(
                    known_encodings,
                    face_encoding
                )

                if len(distances) == 0:
                    current_names.append("Unknown")
                    continue

                best_match_idx = np.argmin(distances)
                best_distance  = distances[best_match_idx]

                if best_distance < TOLERANCE:
                    name = known_names[best_match_idx]
                else:
                    name = "Unknown"

                current_names.append(name)

                # ----------------------------------------
                # EXISTING CONFIRMATION LOGIC
                # ----------------------------------------

                if name != "Unknown":

                    recognition_buffer[name] = (
                        recognition_buffer.get(name, 0) + 1
                    )

                    if recognition_buffer[name] >= CONFIRM_FRAMES:

                        current_time = time.time()

                        if name not in last_recognized:
                            last_recognized[name] = 0

                        if (
                            current_time
                            - last_recognized[name]
                        ) > COOLDOWN:

                            mark_attendance(name)

                            last_recognized[name] = current_time
                            recognition_buffer[name] = 0

                            recognized = True

                            st.success(
                                f"✅ Entry Approved\nWelcome {name}"
                            )

                            break

                else:

                    recognition_buffer = {
                        k: v
                        for k, v in recognition_buffer.items()
                        if k != "Unknown"
                    }

            # ----------------------------------------
            # UNKNOWN SAVE (UNCHANGED)
            # ----------------------------------------

            if "Unknown" in current_names:

                current_time = time.time()

                if (
                    current_time
                    - last_unknown_time
                ) > UNKNOWN_COOLDOWN:

                    os.makedirs(
                        "logs/unknown_faces",
                        exist_ok=True
                    )

                    filename = (
                        datetime.now().strftime(
                            "%Y%m%d%H%M%S"
                        )
                        + ".jpg"
                    )

                    cv2.imwrite(
                        f"logs/unknown_faces/{filename}",
                        frame
                    )

                    last_unknown_time = current_time

                    log_warn(
                        "face-recognition",
                        f"Unknown face saved: {filename}"
                    )

        # ----------------------------------------
        # SHOW CAMERA
        # ----------------------------------------

        cv2.imshow(
            "Smart Hostel Face Scan",
            frame
        )

        if recognized:
            break

        if cv2.waitKey(1) == 13:
            break

    # ---------------------------------------------------
    # CLOSE CAMERA
    # ---------------------------------------------------

    cap.release()
    cv2.destroyAllWindows()

    # ---------------------------------------------------
    # FINAL RESULT
    # ---------------------------------------------------

    if not recognized:

        if timeout:
            st.error(
                "❌ Face Not Found\nAdmin Approval Required"
            )











































