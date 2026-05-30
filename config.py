# Database Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"  # ← replace with your actual MySQL password
DB_NAME = "smart_hostel"
DB_PORT = 3306

# App Configuration
APP_NAME = "Smart Hostel System"
APP_VERSION = "1.0.0"

# Admin Credentials (fallback)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Face Recognition Settings
CONFIDENCE_THRESHOLD = 80
DATASET_PATH = "dataset"
TRAINER_PATH = "trainer/trainer.yml"
ENCODINGS_PATH = "encodings/encodings.pkl"

# Camera Settings
CAMERA_INDEX = 0  # change to 1 or 2 if webcam doesn't open

# Logs
LOG_PATH = "logs/"
UNKNOWN_FACES_PATH = "logs/unknown_faces/"