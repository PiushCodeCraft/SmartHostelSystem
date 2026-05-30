import streamlit as st
from datetime import date
import os
from PIL import Image
import io
from database.database import get_connection
import subprocess

# ---------------------------------------------------
# GENERATE STUDENT ID
# ---------------------------------------------------

def generate_student_id():
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0] + 1
    cursor.close()
    conn.close()
    return f"STU{count:03}"


# ---------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------

def show_add_student():

    st.markdown(
        "<h1 style='margin-bottom:1.2rem'>&#10133; Add Student</h1>",
        unsafe_allow_html=True
    )

    # Init camera state
    if "show_camera" not in st.session_state:
        st.session_state.show_camera = False
    if "captured_photo" not in st.session_state:
        st.session_state.captured_photo = None

    st.markdown(
        "<div style='background:#181c27;border:1px solid #2a2f45;"
        "border-radius:12px;padding:1.4rem'>"
        "<div style='font-size:.88rem;font-weight:600;color:#e8eaf0;margin-bottom:1.2rem'>"
        "New Student Registration</div>",
        unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # BASIC DETAILS
    # ---------------------------------------------------

    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name", placeholder="Riya")
    with col2:
        last_name = st.text_input("Last Name", placeholder="Sharma")

    col3, col4 = st.columns(2)
    with col3:
        room_number = st.text_input("Room Number", placeholder="A-01")
    with col4:
        cls = st.selectbox("Class", ["Select class...", "Class A", "Class B", "Class C", "Class D"])

    col5, col6 = st.columns(2)
    with col5:
        dob = st.date_input("Date of Birth", value=date(2005, 1, 1))
    with col6:
        gender = st.selectbox("Gender", ["Select...", "Male", "Female", "Other"])

    # ---------------------------------------------------
    # GUARDIAN DETAILS
    # ---------------------------------------------------

    col7, col8 = st.columns(2)
    with col7:
        guardian = st.text_input("Guardian Name")
    with col8:
        phone = st.text_input("Guardian Phone")

    address = st.text_input("Address")
    notes   = st.text_area("Additional Notes", height=80)

    # ---------------------------------------------------
    # CAMERA CAPTURE
    # ---------------------------------------------------

    st.markdown(
        "<div style='font-size:.85rem;font-weight:600;color:#e8eaf0;margin:1rem 0 .5rem'>"
        "Student Photo</div>",
        unsafe_allow_html=True
    )

    col_cam1, col_cam2 = st.columns([1, 3])

    with col_cam1:
        # Toggle camera open/close
        if not st.session_state.show_camera:
            if st.button("&#128247; Open Camera", use_container_width=True, type="primary"):
                st.session_state.show_camera    = True
                st.session_state.captured_photo = None
                st.rerun()
        else:
            if st.button("&#10060; Close Camera", use_container_width=True):
                st.session_state.show_camera = False
                st.rerun()

    # Show camera only when open and no photo captured yet
    if st.session_state.show_camera and st.session_state.captured_photo is None:
        st.info("&#128247; Position the student in frame and click **Take Photo**")
        captured = st.camera_input("", label_visibility="collapsed")

        if captured is not None:
            st.session_state.captured_photo = captured
            st.session_state.show_camera    = False
            st.rerun()

    # Show captured photo preview
    if st.session_state.captured_photo is not None:
        col_prev1, col_prev2 = st.columns([1, 3])
        with col_prev1:
            st.image(
                st.session_state.captured_photo,
                caption="Captured Photo",
                width=150
            )
        with col_prev2:
            st.success("&#10003; Photo captured successfully!")
            if st.button("&#128257; Retake Photo", type="secondary"):
                st.session_state.captured_photo = None
                st.session_state.show_camera    = True
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # BUTTONS
    # ---------------------------------------------------

    col_btn1, col_btn2 = st.columns([2, 1])
    with col_btn1:
        submit = st.button("&#10003; Register Student", type="primary", use_container_width=True)
    with col_btn2:
        clear = st.button("Clear", use_container_width=True)

    # ---------------------------------------------------
    # REGISTER STUDENT
    # ---------------------------------------------------

    if submit:

        errors = []

        if not first_name.strip():
            errors.append("First name required")
        if not last_name.strip():
            errors.append("Last name required")
        if cls == "Select class...":
            errors.append("Select a class")
        if gender == "Select...":
            errors.append("Select gender")
        if st.session_state.captured_photo is None:
            errors.append("Capture student photo using the camera")

        if errors:
            for error in errors:
                st.error(error)

        else:
            try:
                student_id   = generate_student_id()
                dataset_path = f"dataset/{student_id}"
                os.makedirs(dataset_path, exist_ok=True)

                # Save captured photo
                image_bytes = st.session_state.captured_photo.getvalue()
                image       = Image.open(io.BytesIO(image_bytes))
                image_path  = f"{dataset_path}/1.jpg"
                image.save(image_path)

                # Insert into DB
                conn   = get_connection()
                cursor = conn.cursor()

                query = """
                    INSERT INTO students (
                        student_id, first_name, last_name, roll_number,
                        room_number, class, gender, dob,
                        guardian_name, guardian_phone, address,
                        photo_path, notes
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """

                values = (
                    student_id,
                    first_name,
                    last_name,
                    student_id,    # roll_number reuses student_id
                    room_number,
                    cls,
                    gender,
                    dob,
                    guardian,
                    phone,
                    address,
                    image_path,
                    notes
                )

                cursor.execute(query, values)
                conn.commit()
                cursor.close()
                conn.close()
                # Auto run encode_faces.py in background
                subprocess.Popen(
                    ["python", "recognition/encode_faces.py"],
                    # stdout=subprocess.DEVNULL,
                    # stderr=subprocess.DEVNULL
                )
                # Clear photo state after successful save
                st.session_state.captured_photo = None
                st.session_state.show_camera    = False

                st.success(f"&#10003; {first_name} {last_name} registered successfully!")
                st.info(f"Student ID: **{student_id}**")
                st.balloons()

            except Exception as e:
                st.error(f"Database Error: {e}")

    # ---------------------------------------------------
    # CLEAR
    # ---------------------------------------------------

    if clear:
        st.session_state.captured_photo = None
        st.session_state.show_camera    = False
        st.rerun()