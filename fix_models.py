# Run this script to patch face_recognition_models __init__.py
# Usage: python fix_models.py

import os
import sys

# Find the installed package path
venv_path = os.path.join(os.path.dirname(sys.executable), '..', 'Lib', 'site-packages')
init_path = os.path.normpath(os.path.join(venv_path, 'face_recognition_models', '__init__.py'))

print(f"Patching: {init_path}")

new_content = '''import os

def pose_predictor_model_location():
    return os.path.join(os.path.dirname(__file__), "models", "shape_predictor_68_face_landmarks.dat")

def pose_predictor_five_point_model_location():
    return os.path.join(os.path.dirname(__file__), "models", "shape_predictor_5_face_landmarks.dat")

def face_recognition_model_location():
    return os.path.join(os.path.dirname(__file__), "models", "dlib_face_recognition_resnet_model_v1.dat")

def cnn_face_detector_model_location():
    return os.path.join(os.path.dirname(__file__), "models", "mmod_human_face_detector.dat")
'''

with open(init_path, 'w') as f:
    f.write(new_content)

print("Done! face_recognition_models patched successfully.")
