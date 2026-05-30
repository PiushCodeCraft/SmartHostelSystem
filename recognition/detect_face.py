import cv2

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(
    'models/haarcascade_frontalface_default.xml'
)

# Start Webcam
cap = cv2.VideoCapture(0)

while True:

    # Read Frame
    ret, frame = cap.read()

    # Convert to Gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect Faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    # Draw Rectangle Around Face
    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (255, 0, 0),
            2
        )

    # Show Camera
    cv2.imshow("Face Detection", frame)

    # Press ENTER to Exit
    if cv2.waitKey(1) == 13:
        break

# Release Camera
cap.release()
cv2.destroyAllWindows()