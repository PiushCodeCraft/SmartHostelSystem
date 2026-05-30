import streamlit as st
from database.database import get_logs, get_unknown_faces

PAGES = {
    "Main": [
        ("📊", "Dashboard"),
        ("🟢", "Current Status"),
        ("📋", "Live Logs"),
        ("📈", "Analytics"),
        ("👤", "Unknown Faces"),
    ],
    "Students": [
        ("👥", "Manage Students"),
        ("➕", "Add Student"),
        ("📄", "Reports"),
    ],
}


def show_sidebar() -> str:
    with st.sidebar:

        st.markdown("""
        <div style='display:flex;align-items:center;gap:10px;padding:4px 0 16px'>
            <span style='font-size:1.5rem'>🏠</span>
            <span style='font-weight:700;font-size:1rem;color:#e8eaf0'>SmartH Admin</span>
        </div>
        <hr style='margin:0 0 12px;border-color:#2a2f45'>
        """, unsafe_allow_html=True)

        selected = st.session_state.get("page", "Dashboard")

        # ── Fetch live badge counts from DB ───────────────────────────────────
        try:
            error_warn_logs   = get_logs(level_filter="WARN",  limit=100)
            error_logs        = get_logs(level_filter="ERROR", limit=100)
            live_log_count    = len(error_warn_logs) + len(error_logs)
        except Exception:
            live_log_count    = 0

        try:
            unknown_list      = get_unknown_faces(resolved=False)
            unknown_count     = len(unknown_list)
        except Exception:
            unknown_count     = 0

        # ── Render nav items ──────────────────────────────────────────────────
        for section, items in PAGES.items():
            st.markdown(
                "<p style='font-size:.68rem;color:#7a82a0;text-transform:uppercase;"
                "letter-spacing:.08em;margin:12px 0 4px'>" + section + "</p>",
                unsafe_allow_html=True,
            )

            for icon, name in items:
                # Build badge dynamically from DB
                badge = ""
                if name == "Live Logs" and live_log_count > 0:
                    badge = f" 🔴 {live_log_count}"
                elif name == "Unknown Faces" and unknown_count > 0:
                    badge = f" 🔴 {unknown_count}"

                label = f"{icon}  {name}{badge}"

                if st.button(label, key=f"nav_{name}", use_container_width=True):
                    st.session_state.page = name
                    selected = name
                    st.rerun()

        # ── Bottom: user info + logout ────────────────────────────────────────
        st.markdown("<hr style='border-color:#2a2f45;margin:16px 0 10px'>", unsafe_allow_html=True)

        username = st.session_state.get("username", "admin")

        st.markdown(
            "<div style='display:flex;align-items:center;gap:10px;margin-bottom:10px'>"
            "<div style='width:32px;height:32px;border-radius:50%;"
            "background:linear-gradient(135deg,#f5a623,#e05252);"
            "display:flex;align-items:center;justify-content:center;"
            "font-size:.75rem;font-weight:700;color:#fff;flex-shrink:0'>"
            + username[:2].upper() +
            "</div>"
            "<div>"
            "<div style='font-size:.83rem;font-weight:600;color:#e8eaf0'>" + username.capitalize() + "</div>"
            "<div style='font-size:.72rem;color:#7a82a0'>Super Admin</div>"
            "</div></div>",
            unsafe_allow_html=True
        )

        if st.button("🚪  Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.query_params.clear()
            st.rerun()

    return st.session_state.get("page", "Dashboard")