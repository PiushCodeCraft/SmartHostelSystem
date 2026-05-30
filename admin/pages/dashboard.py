import streamlit as st
from datetime import datetime

from admin.components.cards import (
    stat_card,
    progress_row
)

from admin.components.charts import (
    attendance_bar_chart
)

from database.database import (
    get_total_students,
    get_present_today,
    get_unknown_faces_today,
    get_camera_counts,
    get_recent_activity
)

import textwrap

# ---------------------------------------------------
# DASHBOARD PAGE
# ---------------------------------------------------

def show_dashboard():
    def render_html(content: str):
        st.markdown(textwrap.dedent(content).strip(), unsafe_allow_html=True)

    # ---------------------------------------------------
    # FETCH DATABASE DATA
    # ---------------------------------------------------

    total_students = get_total_students()

    present_today = get_present_today()

    unknown_faces = get_unknown_faces_today()

    camera_data = get_camera_counts()

    recent_logs = get_recent_activity()

    online = camera_data.get("Online", 0)

    offline = camera_data.get("Offline", 0)

    # ---------------------------------------------------
    # HEADER
    # ---------------------------------------------------
    now = datetime.now().strftime("%d %b %Y, %H:%M")

    st.markdown(
        f"""
        <div style='display:flex;
                    align-items:center;
                    justify-content:space-between;
                    margin-bottom:1.2rem'>
            <div>
                <h1 style='margin:0'>📊 Dashboard</h1>
                <p style='color:#7a82a0; font-size:.83rem; margin:2px 0 0'>
                    Welcome back, {st.session_state.get('username','Admin').capitalize()}
                </p>
            </div>
            <div style='background:#181c27;
                        border:1px solid #2a2f45;
                        border-radius:8px;
                        padding:.4rem .9rem;
                        font-size:.8rem;
                        color:#7a82a0'>
                {now}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # ---------------------------------------------------
    # STAT CARDS
    # ---------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        stat_card(
            "👥 Total Students",
            str(total_students),
            "Registered Students",
            "#e8eaf0"
        )

    with c2:
        attendance_percentage = 0

        if total_students > 0:
            attendance_percentage = round(
                (present_today / total_students) * 100,
                1
            )

        stat_card(
            "✅ Students IN",
            str(present_today),
            f"{attendance_percentage}% inside hostel",
            "#3ecf8e"
        )

    with c3:
        stat_card(
            "👤 Unknown Faces",
            str(unknown_faces),
            "Security alerts detected",
            "#f5a623"
        )

    with c4:
        stat_card(
            "📷 Cameras Online",
            f"{online}/{online + offline}",
            f"{offline} offline",
            "#4f8ef7"
        )

    render_html(
        "<div style='margin:1rem 0'></div>"
    )

    # ---------------------------------------------------
    # CHART + SYSTEM HEALTH
    # ---------------------------------------------------

    col_chart, col_health = st.columns([2, 1])

    # ---------------------------------------------------
    # ATTENDANCE CHART
    # ---------------------------------------------------

    with col_chart:
        st.markdown(
            """
            <div style='background:#181c27;
                        border:1px solid #2a2f45;
                        border-radius:12px;
                        padding:1rem 1.2rem;
                        height:100%'>
                <div style='font-size:.85rem;
                            font-weight:600;
                            color:#e8eaf0;
                            margin-bottom:.8rem'>
                    Weekly Attendance
                    <span style='font-size:.72rem;
                                color:#7a82a0;
                                font-weight:400'>
                        Mon &ndash; Sun
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        attendance_bar_chart()

    # ---------------------------------------------------
    # SYSTEM HEALTH
    # ---------------------------------------------------

    with col_health:
        st.markdown(
            """
            <div style='font-size:.85rem;
                        font-weight:600;
                        color:#e8eaf0;
                        margin-bottom:1rem'>
                System Health
            </div>
            """,
            unsafe_allow_html=True
        )

        progress_row("CPU Usage", 34, "#4f8ef7")
        progress_row("Memory",    61, "#f5a623")
        progress_row("Storage",   48, "#3ecf8e")
        progress_row("Network",   74, "#ff5c8a")

    render_html(
        "<div style='margin:1rem 0'></div>"
    )

    # ---------------------------------------------------
    # RECENT ACTIVITY
    # ---------------------------------------------------

    st.markdown(
        """
        <div style='font-size:.85rem;
                    font-weight:600;
                    color:#e8eaf0;
                    margin-bottom:1rem'>
            Recent Activity
            <span style='font-size:.72rem;
                        color:#7a82a0;
                        font-weight:400'>
                Live System Logs
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # SHOW LOGS
    # ---------------------------------------------------

    if recent_logs:

        for log in recent_logs:

            level = log["level"]
            icon = "🔵"

            if level == "INFO":
                icon = "🟢"
            elif level == "WARN":
                icon = "🟡"
            elif level == "ERROR":
                icon = "🔴"

            timestamp = log["timestamp"].strftime("%H:%M")

            st.markdown(
                f"""
                <div style='display:flex;
                            align-items:center;
                            gap:10px;
                            padding:.7rem 0;
                            border-bottom:1px solid #2a2f45;
                            font-size:.83rem'>
                    <span>{icon}</span>
                    <span style='flex:1; color:#e8eaf0'>{log['message']}</span>
                    <span style='color:#7a82a0; font-size:.72rem'>{timestamp}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.info("No activity logs found")
