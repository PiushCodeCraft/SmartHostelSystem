import streamlit as st
from database.database import run_query


# ── Fetch Unknown Faces from DB ───────────────────────────────────────────────

def get_unknown_faces():
    query = """
        SELECT id, location, camera, confidence, detected_at, is_resolved
        FROM unknown_faces
        ORDER BY detected_at DESC
    """
    rows = run_query(query)
    faces = []
    for row in rows:
        detected_time = row["detected_at"].strftime("%I:%M %p") if row["detected_at"] else ""
        faces.append({
            "id":         f"UF-{row['id']:03d}",
            "raw_id":     row["id"],
            "location":   row["location"] or "Unknown Area",
            "time":       detected_time,
            "camera":     row["camera"] or "Unknown Cam",
            "confidence": int(row["confidence"] or 0),
            "resolved":   row["is_resolved"]
        })
    return faces


# ── Main Page ─────────────────────────────────────────────────────────────────

def show_unknown_faces():

    FACES = get_unknown_faces()

    st.markdown("<h1 style='margin-bottom:.4rem'>&#128100; Unknown Faces</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#7a82a0;font-size:.85rem;margin-bottom:1.2rem'>"
        "Unrecognised faces detected in the last 24 hours. Review and take action.</p>",
        unsafe_allow_html=True
    )

    if not FACES:
        st.info("No unknown faces detected.")
        return

    cols = st.columns(4)

    for i, face in enumerate(FACES):
        with cols[i % 4]:

            conf      = face["confidence"]
            conf_color = "#3ecf8e" if conf >= 90 else "#f5a623"
            loc       = face["location"]
            time_cam  = f"{face['time']} &middot; {face['camera']}"
            fid       = face["id"]

            # Build card HTML using string concatenation to avoid f-string nesting issues
            card = (
                "<div style='background:#181c27;border:1px solid #2a2f45;"
                "border-radius:12px;padding:1.2rem 1rem;text-align:center;margin-bottom:12px'>"

                "<div style='width:60px;height:60px;border-radius:50%;background:#1e2233;"
                "border:2px solid #2a2f45;display:flex;align-items:center;"
                "justify-content:center;font-size:1.6rem;margin:0 auto .8rem'>&#128100;</div>"

                "<div style='font-size:.85rem;font-weight:600;color:#e8eaf0'>" + loc + "</div>"

                "<div style='font-size:.75rem;color:#7a82a0;margin-top:.2rem'>" + time_cam + "</div>"

                "<div style='margin-top:.5rem'>"
                "<span style='background:rgba(79,142,247,.12);color:" + conf_color + ";"
                "padding:2px 8px;border-radius:4px;font-size:.72rem;font-weight:600'>"
                "Conf: " + str(conf) + "%</span></div>"

                "<div style='font-size:.7rem;color:#7a82a0;margin-top:.3rem'>" + fid + "</div>"

                "</div>"
            )

            st.markdown(card, unsafe_allow_html=True)

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("&#128269; Identify", key=f"id_{fid}", use_container_width=True):
                    st.toast(f"Searching for match… ({fid})", icon="🔍")
            with col_b:
                if st.button("&#128680; Alert", key=f"al_{fid}", use_container_width=True):
                    st.toast(f"Security alerted for {fid}", icon="🚨")

    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

    # ── Summary Bar ───────────────────────────────────────────────────────────

    pending  = len([f for f in FACES if not f["resolved"]])
    avg_conf = round(sum(f["confidence"] for f in FACES) / len(FACES), 1) if FACES else 0

    summary = (
        "<div style='background:#181c27;border:1px solid #2a2f45;border-radius:10px;"
        "padding:.8rem 1.2rem;display:flex;gap:2rem;align-items:center'>"

        "<div><div style='font-size:.72rem;color:#7a82a0'>Total Today</div>"
        "<div style='font-size:1.2rem;font-weight:700;color:#f5a623'>" + str(len(FACES)) + "</div></div>"

        "<div><div style='font-size:.72rem;color:#7a82a0'>Pending Review</div>"
        "<div style='font-size:1.2rem;font-weight:700;color:#e05252'>" + str(pending) + "</div></div>"

        "<div><div style='font-size:.72rem;color:#7a82a0'>Avg Confidence</div>"
        "<div style='font-size:1.2rem;font-weight:700;color:#4f8ef7'>" + str(avg_conf) + "%</div></div>"

        "</div>"
    )

    st.markdown(summary, unsafe_allow_html=True)