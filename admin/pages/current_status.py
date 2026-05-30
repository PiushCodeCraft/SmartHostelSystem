import streamlit as st
from database.database import get_location_status


# Fetch Current Status from DB
def get_locations():

    rows = get_location_status()

    locations = []

    for row in rows:

        name     = row["location_name"]
        count    = row["current_count"]
        capacity = row["capacity"]
        status   = row["status"]

        # Default styling
        dot_color = "#3ecf8e"
        color     = "#3ecf8e"
        pct       = None
        bar_color = "#3ecf8e"
        detail    = ""

        # Entrance / Gate
        if name in ["Main Entrance", "Gate B"]:
            detail = f"Status: {status}"
            if status.lower() == "locked":
                dot_color = "#e05252"
                color     = "#e05252"

        # Capacity based cards
        elif capacity > 0:
            pct    = int((count / capacity) * 100)
            detail = f"Capacity: {capacity}"
            if name == "Cafeteria":
                dot_color = "#f5a623"
                color     = "#f5a623"
                bar_color = "#f5a623"

        # Server Room
        elif name == "Server Room":
            detail = "System Normal"
            if status.lower() == "locked":
                dot_color = "#e05252"
                color     = "#e05252"
            else:
                dot_color = "#4f8ef7"
                color     = "#4f8ef7"

        locations.append({
            "name":      name,
            "status":    f"{count} inside" if capacity > 0 else status,
            "detail":    detail,
            "dot_color": dot_color,
            "color":     color,
            "pct":       pct,
            "bar_color": bar_color,
        })

    return locations


def show_current_status():

    LOCATIONS = get_locations()

    st.markdown(
        "<h1 style='margin-bottom:1.2rem'>&#128994; Current Status</h1>",
        unsafe_allow_html=True
    )

    cols = st.columns(3)

    for i, loc in enumerate(LOCATIONS):
        with cols[i % 3]:

            if loc.get("pct") is not None:
                pct       = loc["pct"]
                bar_color = loc.get("bar_color", "#4f8ef7")
                bar_html  = (
                    f"<div style='height:5px;background:#1e2233;border-radius:3px;"
                    f"overflow:hidden;margin-top:.6rem'>"
                    f"<div style='height:100%;width:{pct}%;background:{bar_color};"
                    f"border-radius:3px'></div></div>"
                )
            else:
                bar_html = ""

            html = (
                f"<div style='background:#181c27;border:1px solid #2a2f45;"
                f"border-radius:12px;padding:1.1rem;margin-bottom:12px'>"
                f"<div style='display:flex;justify-content:space-between;"
                f"align-items:center;margin-bottom:.6rem'>"
                f"<span style='font-size:.85rem;font-weight:600;color:#e8eaf0'>"
                f"{loc['name']}</span>"
                f"<span style='width:10px;height:10px;border-radius:50%;"
                f"background:{loc['dot_color']};display:inline-block'></span>"
                f"</div>"
                f"<div style='font-size:1.3rem;font-weight:700;color:{loc['color']};"
                f"margin-bottom:.2rem'>{loc['status']}</div>"
                f"<div style='font-size:.76rem;color:#7a82a0'>{loc['detail']}</div>"
                f"{bar_html}"
                f"</div>"
            )

            st.markdown(html, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:.5rem'></div>", unsafe_allow_html=True)

    if st.button("🔄  Refresh Status", type="primary"):
        st.rerun()