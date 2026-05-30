# Smart Hostel Entry & Exit System using Face Recognition

## Project Overview

The Smart Hostel Entry & Exit System is an AI-based hostel security and monitoring system that automates hostel entry and exit monitoring using Face Recognition and Computer Vision.

The system replaces:

* Manual attendance registers
* ID card checking
* Manual signatures

with a secure automated face scanning system.

When a student approaches the hostel gate:

1. Student clicks **Scan Face**
2. Camera opens for 30 seconds
3. System detects and recognizes the face
4. Student identity is verified
5. IN/OUT status is updated automatically
6. Date and time are stored in the database
7. Camera closes automatically

Only the Admin/Warden has access to the management dashboard.

---

# Features

## Student Features

* Face-based entry and exit
* Scan Face button interface
* Automatic attendance logging
* Real-time recognition
* Camera auto closes after recognition
* No manual signature required

## Admin Features

* Secure admin login
* Add and manage students
* Automatic face encoding after registration
* View hostel logs
* Monitor IN/OUT status
* Unknown person detection
* View reports and records
* Admin approval for unknown faces

---

# Technologies Used

| Technology       | Purpose                    |
| ---------------- | -------------------------- |
| Python           | Main Programming Language  |
| OpenCV           | Face Detection             |
| face_recognition | Face Recognition           |
| MySQL            | Database Management        |
| Streamlit        | Dashboard & Recognition UI |
| Haar Cascade     | Face Detection Model       |

---

# Project Structure

SmartHostelSystem/
│
├── app.py
├── config.py
├── capture_photos.py
├── requirements.txt
├── README.md
│
├── dataset/
├── encodings/
├── logs/
├── database/
├── models/
├── recognition/
├── admin/
└── utils/

---

# Recognition Workflow

Student Clicks Scan Face
↓
Camera Opens (30 sec only)
↓
Face Detection
↓
Face Recognition
↓
Compare with Stored Encodings
↓
Known Student ?
↓              ↓
YES             NO
↓                ↓
Mark IN/OUT    Save Unknown Face
↓                ↓
Show Success   Admin Approval Required
↓
Store Date & Time
↓
Close Camera Automatically

---

# Database Tables

## Admin Table

| Field    | Description    |
| -------- | -------------- |
| admin_id | Admin ID       |
| username | Admin username |
| password | Admin password |

## Students Table

| Field       | Description     |
| ----------- | --------------- |
| student_id  | Student ID      |
| first_name  | First Name      |
| last_name   | Last Name       |
| room_number | Room Number     |
| class       | Student Class   |
| gender      | Gender          |
| photo_path  | Face Image Path |

## Hostel Logs Table

| Field        | Description  |
| ------------ | ------------ |
| id           | Log ID       |
| student_name | Student Name |
| date         | Entry Date   |
| time         | Entry Time   |
| status       | IN/OUT       |

---

# Installation

## Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# Commands to Run the Project

## Step 1 — Activate Virtual Environment

```powershell
cd D:\github\SmartHostelSystem
venv\Scripts\activate
```

---

## Step 2 — Start Admin Dashboard

```powershell
streamlit run app.py --server.port 8501
```

Open:

http://localhost:8501

---

## Step 3 — Start Face Recognition Page

Recognition runs on separate port:

```powershell
streamlit run recognition\recognize_face.py --server.port 8502
```

Open:

http://localhost:8502

---

# Daily Run Commands

## Terminal 1 — Admin Dashboard

```powershell
cd D:\github\SmartHostelSystem
venv\Scripts\activate
streamlit run app.py --server.port 8501
```

---

## Terminal 2 — Face Recognition

```powershell
cd D:\github\SmartHostelSystem
venv\Scripts\activate
streamlit run recognition\recognize_face.py --server.port 8502
```

---

# Student Registration Workflow

When a new student is added:

1. Register student using Admin Dashboard
2. Capture student photo
3. Photo saves in dataset/
4. encode_faces.py runs automatically
5. Face encodings update automatically
6. Student becomes ready for recognition

No manual encoding command required.

---

# Optional Commands

## Capture Additional Photos

For better recognition accuracy:

```powershell
python capture_photos.py STU001
```

## Manual Encoding (Optional)

```powershell
python recognition\encode_faces.py
```

---

# Conclusion

The Smart Hostel Entry & Exit System provides a secure, efficient, and intelligent solution for hostel management using Artificial Intelligence and Computer Vision.

The system automates student verification and attendance tracking while improving security, reducing manual work, and enabling smarter hostel monitoring.
