import streamlit as st
import time
from database.database import verify_login


def show_login():

    st.markdown("""
    <div style='display:flex;justify-content:center;margin-top:80px'>
        <div style='text-align:center;margin-bottom:10px'>
            <div style='font-size:2.5rem'>🏠</div>
            <h2 style='margin:0;font-size:1.6rem;font-weight:700;color:#e8eaf0'>SmartH Admin</h2>
            <p style='color:#7a82a0;font-size:.9rem;margin-top:4px'>Sign in to your control panel</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        username = st.text_input("Username", placeholder="admin", key="login_user")
        password = st.text_input("Password", placeholder="••••••••", type="password", key="login_pass")

        if st.button("Sign In", use_container_width=True, type="primary"):

            db_valid      = verify_login(username, password)
            fallback_valid = (username == "admin" and password == "admin123") or \
                             (username == "piush" and password == "piush123")

            if db_valid or fallback_valid:
                st.session_state.logged_in   = True
                st.session_state.username    = username
                st.session_state.page        = "Dashboard"
                st.session_state.last_active = time.time()
                # Store in query params so session survives page reload
                st.query_params["user"] = username
                st.query_params["auth"] = "1"
                st.rerun()
            else:
                st.error("Invalid username or password.")

        st.markdown(
            "<p style='text-align:center;color:#7a82a0;font-size:.75rem;margin-top:8px'>"
            "Demo credentials: admin / admin123</p>",
            unsafe_allow_html=True,
        )