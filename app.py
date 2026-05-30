import streamlit as st
import time

st.set_page_config(
    page_title="SmartH Admin",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load CSS safely
try:
    with open("admin/styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# ── Session State Defaults ────────────────────────────────────────────────────

if "logged_in"   not in st.session_state: st.session_state.logged_in   = False
if "page"        not in st.session_state: st.session_state.page        = "Dashboard"
if "username"    not in st.session_state: st.session_state.username    = ""
if "last_active" not in st.session_state: st.session_state.last_active = time.time()

# ── Restore session from query params (survives reload) ───────────────────────

params = st.query_params

if not st.session_state.logged_in:
    # Check if login info is stored in URL params
    if params.get("user") and params.get("auth") == "1":
        st.session_state.logged_in   = True
        st.session_state.username    = params.get("user")
        st.session_state.last_active = time.time()

# ── Inactivity Timeout (10 minutes) ──────────────────────────────────────────

TIMEOUT_SECONDS = 10 * 60  # 10 minutes

if st.session_state.logged_in:
    elapsed = time.time() - st.session_state.last_active
    if elapsed > TIMEOUT_SECONDS:
        # Clear everything including query params
        st.session_state.logged_in   = False
        st.session_state.username    = ""
        st.session_state.page        = "Dashboard"
        st.session_state.last_active = time.time()
        st.query_params.clear()
        st.warning("⏱️ You were logged out due to 10 minutes of inactivity.")
        st.rerun()
    else:
        # Refresh activity timer on every interaction
        st.session_state.last_active = time.time()

# ── LOGIN GATE ────────────────────────────────────────────────────────────────

if not st.session_state.logged_in:
    from login import show_login
    show_login()
    st.stop()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────

from admin.components.sidebar import show_sidebar
page = show_sidebar()

# ── PAGE ROUTING ──────────────────────────────────────────────────────────────

if page == "Dashboard":
    from admin.pages.dashboard import show_dashboard
    show_dashboard()
elif page == "Current Status":
    from admin.pages.current_status import show_current_status
    show_current_status()
elif page == "Live Logs":
    from admin.pages.live_logs import show_live_logs
    show_live_logs()
elif page == "Analytics":
    from admin.pages.analytics import show_analytics
    show_analytics()
elif page == "Unknown Faces":
    from admin.pages.unknown_faces import show_unknown_faces
    show_unknown_faces()
elif page == "Manage Students":
    from admin.pages.manage_students import show_manage_students
    show_manage_students()
elif page == "Add Student":
    from admin.pages.add_student import show_add_student
    show_add_student()
elif page == "Reports":
    from admin.pages.reports import show_reports
    show_reports()