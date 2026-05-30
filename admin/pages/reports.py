import streamlit as st
from datetime import date
from database.database import run_query


# ── Fetch report data from DB ─────────────────────────────────────────────────

def get_reports():
    reports = []

    attendance = run_query("SELECT COUNT(*) as total FROM attendance")
    total_att  = attendance[0]["total"] if attendance else 0
    reports.append({
        "icon":  "&#128202;",
        "title": "Attendance Report",
        "sub":   f"{total_att} attendance logs",
        "type":  "Attendance",
        "size":  f"{max(20, total_att)} KB",
        "color": "rgba(79,142,247,.15)",
        "fc":    "#4f8ef7"
    })

    unknown    = run_query("SELECT COUNT(*) as total, SUM(CASE WHEN is_resolved=0 THEN 1 ELSE 0 END) as pending FROM unknown_faces")
    uf_total   = unknown[0]["total"]   or 0
    uf_pending = unknown[0]["pending"] or 0
    reports.append({
        "icon":  "&#128100;",
        "title": "Unknown Faces Report",
        "sub":   f"{uf_total} incidents &middot; {uf_pending} pending review",
        "type":  "Security",
        "size":  f"{max(20, uf_total*3)} KB",
        "color": "rgba(245,166,35,.15)",
        "fc":    "#f5a623"
    })

    students       = run_query("SELECT COUNT(*) as total FROM students WHERE is_active=1")
    total_students = students[0]["total"] if students else 0
    reports.append({
        "icon":  "&#127891;",
        "title": "Student Summary Report",
        "sub":   f"{total_students} active students",
        "type":  "Students",
        "size":  f"{max(30, total_students*2)} KB",
        "color": "rgba(62,207,142,.15)",
        "fc":    "#3ecf8e"
    })

    locations       = run_query("SELECT COUNT(*) as total FROM location_status")
    total_locations = locations[0]["total"] if locations else 0
    reports.append({
        "icon":  "&#128205;",
        "title": "System Status Report",
        "sub":   f"{total_locations} monitored locations",
        "type":  "Hardware",
        "size":  f"{max(20, total_locations*2)} KB",
        "color": "rgba(108,99,255,.15)",
        "fc":    "#6c63ff"
    })

    return reports


# ── Main Page ─────────────────────────────────────────────────────────────────

def show_reports():

    REPORTS = get_reports()

    st.markdown(
        "<h1 style='margin-bottom:.4rem'>&#128196; Reports</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='color:#7a82a0;font-size:.85rem;margin-bottom:1.2rem'>"
        "Download or generate reports for attendance, security, and system health.</p>",
        unsafe_allow_html=True
    )

    # ── Generate New Report ───────────────────────────────────────────────────

    with st.expander("&#128260; Generate New Report"):
        gc1, gc2, gc3 = st.columns(3)
        with gc1:
            rtype = st.selectbox("Report Type", ["Attendance", "Security", "Students", "Hardware"])
        with gc2:
            start = st.date_input("From", value=date.today())
        with gc3:
            end = st.date_input("To", value=date.today())

        if st.button("&#9881; Generate", type="primary"):
            st.success(f"&#10003; {rtype} report from {start} to {end} generated successfully!")

    st.markdown("<div style='margin:.8rem 0'></div>", unsafe_allow_html=True)

    # ── Report List ───────────────────────────────────────────────────────────

    for report in REPORTS:

        col_icon, col_info, col_meta, col_btn = st.columns([0.4, 4, 1.5, 1])

        with col_icon:
            st.markdown(
                "<div style='width:40px;height:40px;border-radius:9px;"
                "background:" + report["color"] + ";display:flex;align-items:center;"
                "justify-content:center;font-size:1.2rem;margin-top:4px'>"
                + report["icon"] + "</div>",
                unsafe_allow_html=True
            )

        with col_info:
            st.markdown(
                "<div style='padding:4px 0'>"
                "<div style='font-size:.9rem;font-weight:600;color:#e8eaf0'>"
                + report["title"] + "</div>"
                "<div style='font-size:.76rem;color:#7a82a0;margin-top:2px'>"
                + report["sub"] + "</div>"
                "</div>",
                unsafe_allow_html=True
            )

        with col_meta:
            st.markdown(
                "<div style='padding:4px 0;text-align:right'>"
                "<span style='background:" + report["color"] + ";color:" + report["fc"] + ";"
                "padding:2px 8px;border-radius:4px;font-size:.72rem;font-weight:600'>"
                + report["type"] + "</span>"
                "<div style='font-size:.72rem;color:#7a82a0;margin-top:4px'>"
                + report["size"] + "</div>"
                "</div>",
                unsafe_allow_html=True
            )

        with col_btn:
            if st.button("&#11015; Download", key=f"dl_{report['title']}", use_container_width=True):
                st.toast(f"Downloading: {report['title']}", icon="📥")

        st.markdown(
            "<hr style='border-color:#2a2f45;margin:.5rem 0'>",
            unsafe_allow_html=True
        )