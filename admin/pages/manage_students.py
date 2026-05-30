import streamlit as st
from database.database import get_all_students, get_classes, delete_student, run_query


def show_manage_students():
    st.markdown(
        "<h1 style='margin-bottom:1rem'>&#128101; Manage Students</h1>",
        unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # FILTERS
    # ---------------------------------------------------

    col_search, col_class, col_status, col_refresh = st.columns([3, 1.5, 1.5, 1])

    with col_search:
        search = st.text_input(
            "", placeholder="Search by name or ID...",
            label_visibility="collapsed"
        )

    with col_class:
        db_classes = get_classes()
        class_opts = ["All Classes"] + db_classes
        cls_filter = st.selectbox("", class_opts, label_visibility="collapsed")

    with col_status:
        status_filter = st.selectbox(
            "", ["All Status", "Present", "Absent"],
            label_visibility="collapsed"
        )

    with col_refresh:
        if st.button("🔄", help="Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    # ---------------------------------------------------
    # FETCH FROM DATABASE (always fresh)
    # ---------------------------------------------------

    data = get_all_students(
        search        = search,
        class_filter  = cls_filter,
        status_filter = status_filter,
    )

    # ---------------------------------------------------
    # SUMMARY COUNTS
    # ---------------------------------------------------

    present = sum(1 for d in data if d["status"] == "Present")
    absent  = sum(1 for d in data if d["status"] == "Absent")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Shown", len(data))
    c2.metric("Present",     present)
    c3.metric("Absent",      absent)

    st.markdown("<div style='margin:.6rem 0'></div>", unsafe_allow_html=True)

    STATUS_COLORS = {
        "Present": ("rgba(62,207,142,.15)", "#3ecf8e"),
        "Absent":  ("rgba(224,82,82,.15)",  "#e05252"),
    }

    # ---------------------------------------------------
    # TABLE HEADER
    # ---------------------------------------------------

    st.markdown("""
        <div style='background:#181c27;border:1px solid #2a2f45;
                    border-radius:12px;overflow:hidden'>
            <div style='display:grid;
                        grid-template-columns:90px 1fr 100px 90px 100px 110px 80px;
                        padding:.5rem .9rem;border-bottom:1px solid #2a2f45;
                        background:#1e2233'>
                <span style='font-size:.72rem;color:#7a82a0;text-transform:uppercase'>ID</span>
                <span style='font-size:.72rem;color:#7a82a0;text-transform:uppercase'>Name</span>
                <span style='font-size:.72rem;color:#7a82a0;text-transform:uppercase'>Class</span>
                <span style='font-size:.72rem;color:#7a82a0;text-transform:uppercase'>Room No.</span>
                <span style='font-size:.72rem;color:#7a82a0;text-transform:uppercase'>Status</span>
                <span style='font-size:.72rem;color:#7a82a0;text-transform:uppercase'>Last Seen</span>
                <span style='font-size:.72rem;color:#7a82a0;text-transform:uppercase'>Action</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # TABLE ROWS
    # ---------------------------------------------------

    if data:
        for s in data:
            bg, fg    = STATUS_COLORS.get(s["status"], ("transparent", "#e8eaf0"))
            full_name = s["first_name"] + " " + s["last_name"]
            room      = s["room_number"] or "-"

            row_html = (
                "<div style='display:grid;"
                "grid-template-columns:90px 1fr 100px 90px 100px 110px 80px;"
                "padding:.55rem .9rem;border-bottom:1px solid #2a2f45;"
                "font-size:.83rem;align-items:center'>"
                "<span style='color:#7a82a0;font-size:.78rem'>" + s["student_id"] + "</span>"
                "<span style='color:#e8eaf0;font-weight:500'>" + full_name + "</span>"
                "<span style='color:#e8eaf0'>" + s["class"] + "</span>"
                "<span style='color:#7a82a0'>" + room + "</span>"
                "<span><span style='background:" + bg + ";color:" + fg + ";"
                "padding:2px 8px;border-radius:4px;font-size:.72rem;font-weight:600'>"
                + s["status"] + "</span></span>"
                "<span style='color:#7a82a0;font-size:.78rem'>" + s["last_seen"] + "</span>"
                "<span></span>"
                "</div>"
            )

            st.markdown(row_html, unsafe_allow_html=True)

            # Delete button aligned to last column
            _, btn_col = st.columns([11, 1])
            with btn_col:
                if st.button(
                    "🗑️",
                    key=f"del_{s['student_id']}",
                    help=f"Remove {full_name}"
                ):
                    # Hard delete from DB so it's immediately gone
                    deleted = run_query(
                        "DELETE FROM students WHERE student_id=%s",
                        (s["student_id"],),
                        fetch=False
                    )
                    if deleted:
                        st.success(f"Removed {full_name}")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Failed to remove student")

    else:
        st.markdown(
            "<div style='padding:2rem;text-align:center;color:#7a82a0;font-size:.85rem'>"
            "No students match your search.</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:.75rem;color:#7a82a0;margin-top:.5rem'>"
        + str(len(data)) + " students shown</p>",
        unsafe_allow_html=True
    )