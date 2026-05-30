import streamlit as st
from database.database import get_logs


def show_live_logs():
    st.markdown("<h1 style='margin-bottom:1rem'>&#128203; Live Logs</h1>", unsafe_allow_html=True)

    # ── Filters ───────────────────────────────────────────────────────────────

    col_f1, col_f2, col_f3, col_f4, col_search = st.columns([1, 1, 1, 1, 3])

    if "log_filter" not in st.session_state:
        st.session_state.log_filter = "all"

    with col_f1:
        if st.button("All", use_container_width=True,
                     type="primary" if st.session_state.log_filter == "all" else "secondary"):
            st.session_state.log_filter = "all"; st.rerun()

    with col_f2:
        if st.button("&#128309; Info", use_container_width=True,
                     type="primary" if st.session_state.log_filter == "INFO" else "secondary"):
            st.session_state.log_filter = "INFO"; st.rerun()

    with col_f3:
        if st.button("&#128993; Warn", use_container_width=True,
                     type="primary" if st.session_state.log_filter == "WARN" else "secondary"):
            st.session_state.log_filter = "WARN"; st.rerun()

    with col_f4:
        if st.button("&#128308; Error", use_container_width=True,
                     type="primary" if st.session_state.log_filter == "ERROR" else "secondary"):
            st.session_state.log_filter = "ERROR"; st.rerun()

    with col_search:
        search = st.text_input("", placeholder="Search logs...", label_visibility="collapsed")

    # ── Fetch from Database ───────────────────────────────────────────────────

    active_filter = st.session_state.log_filter
    all_logs      = get_logs(level_filter=active_filter, search=search, limit=100)
    total_logs    = get_logs(limit=100)  # for total count display

    # ── Table ─────────────────────────────────────────────────────────────────

    st.markdown(
        "<div style='background:#181c27;border:1px solid #2a2f45;border-radius:12px;"
        "overflow:hidden;margin-top:.8rem'>"
        "<div style='display:grid;grid-template-columns:140px 80px 160px 1fr;"
        "padding:.5rem .8rem;border-bottom:1px solid #2a2f45'>"
        "<span style='font-size:.72rem;color:#7a82a0;text-transform:uppercase;letter-spacing:.04em'>Time</span>"
        "<span style='font-size:.72rem;color:#7a82a0;text-transform:uppercase;letter-spacing:.04em'>Level</span>"
        "<span style='font-size:.72rem;color:#7a82a0;text-transform:uppercase;letter-spacing:.04em'>Source</span>"
        "<span style='font-size:.72rem;color:#7a82a0;text-transform:uppercase;letter-spacing:.04em'>Message</span>"
        "</div>",
        unsafe_allow_html=True
    )

    TAG_COLORS = {
        "INFO":  ("rgba(79,142,247,.15)",  "#4f8ef7"),
        "WARN":  ("rgba(245,166,35,.15)",  "#f5a623"),
        "ERROR": ("rgba(224,82,82,.15)",   "#e05252"),
    }

    if all_logs:
        for log in all_logs:
            bg, fg    = TAG_COLORS.get(log["level"], ("transparent", "#e8eaf0"))
            timestamp = log["timestamp"].strftime("%Y-%m-%d %H:%M:%S") if log["timestamp"] else "-"
            level     = log["level"]   or "INFO"
            source    = log["source"]  or "-"
            message   = log["message"] or "-"

            row = (
                "<div style='display:grid;grid-template-columns:140px 80px 160px 1fr;"
                "padding:.55rem .8rem;border-bottom:1px solid #2a2f45;font-size:.82rem'>"
                "<span style='color:#7a82a0;font-family:monospace;font-size:.76rem'>" + timestamp + "</span>"
                "<span><span style='background:" + bg + ";color:" + fg + ";padding:2px 8px;"
                "border-radius:4px;font-size:.72rem;font-weight:600'>" + level + "</span></span>"
                "<span style='color:#7a82a0;font-size:.78rem'>" + source + "</span>"
                "<span style='color:#e8eaf0'>" + message + "</span>"
                "</div>"
            )
            st.markdown(row, unsafe_allow_html=True)

    else:
        st.markdown(
            "<div style='padding:2rem;text-align:center;color:#7a82a0;font-size:.85rem'>"
            "No logs match the current filter.</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size:.75rem;color:#7a82a0;margin-top:.5rem'>Showing "
        + str(len(all_logs)) + " of " + str(len(total_logs)) + " entries</p>",
        unsafe_allow_html=True
    )

    # ── Refresh Button ────────────────────────────────────────────────────────

    if st.button("&#128260; Refresh Logs", type="primary"):
        st.rerun()