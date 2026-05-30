import streamlit as st
import plotly.graph_objects as go
from datetime import date, timedelta

# ── Shared theme ──────────────────────────────────────────────────────────────

_BG        = "#181c27"
_GRID      = "#2a2f45"
_TEXT      = "#7a82a0"
_BAR_COLOR = "#4f8ef7"
_TODAY_BAR = "#7eb3ff"

_LAYOUT = dict(
    paper_bgcolor = _BG,
    plot_bgcolor  = _BG,
    font          = dict(color=_TEXT, size=11),
    margin        = dict(l=10, r=10, t=10, b=30),
    xaxis         = dict(gridcolor=_GRID, zeroline=False),
    yaxis         = dict(gridcolor=_GRID, zeroline=False),
)


# ── Weekly attendance bar (dashboard) ─────────────────────────────────────────

def attendance_bar_chart(data: list | None = None):
    """
    data: list of dicts with keys 'date' (date) and 'count' (int).
    Falls back to zeros if None.
    """
    if data:
        labels = [d["date"].strftime("%a") for d in data]
        values = [d["count"] for d in data]
    else:
        labels = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        values = [0] * 7

    today_label = date.today().strftime("%a")
    colors = [_TODAY_BAR if l == today_label else _BAR_COLOR for l in labels]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        hovertemplate="%{x}: %{y} students<extra></extra>",
    ))
    fig.update_layout(**_LAYOUT, height=220)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ── Monthly attendance bar (analytics) ───────────────────────────────────────

def monthly_attendance_chart(data: list | None = None):
    """
    data: list of 12 ints, one per month (Jan–Dec).
    Falls back to zeros if None.
    """
    months = ["Jan","Feb","Mar","Apr","May","Jun",
              "Jul","Aug","Sep","Oct","Nov","Dec"]
    values = data if (data and len(data) == 12) else [0] * 12

    fig = go.Figure(go.Bar(
        x=months, y=values,
        marker_color=_BAR_COLOR,
        hovertemplate="%{x}: %{y} present<extra></extra>",
    ))
    fig.update_layout(**_LAYOUT, height=240)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ── Hourly entry bar (analytics) ─────────────────────────────────────────────

def hourly_entry_chart(data: list | None = None):
    """
    data: list of 24 ints, one per hour (0–23).
    Falls back to zeros if None.
    """
    hours  = [f"{h:02d}:00" for h in range(24)]
    values = data if (data and len(data) == 24) else [0] * 24

    fig = go.Figure(go.Bar(
        x=hours, y=values,
        marker_color="#3ecf8e",
        hovertemplate="%{x}: %{y} entries<extra></extra>",
    ))
    fig.update_layout(**_LAYOUT, height=240)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ── 30-day trend line (analytics) ────────────────────────────────────────────

def attendance_line_chart(data: list | None = None):
    """
    data: list of 30 ints (oldest → newest).
    Falls back to zeros if None.
    """
    labels = [(date.today() - timedelta(days=29-i)).strftime("%d %b")
              for i in range(30)]
    values = data if (data and len(data) == 30) else [0] * 30

    fig = go.Figure(go.Scatter(
        x=labels, y=values,
        mode="lines+markers",
        line=dict(color=_BAR_COLOR, width=2),
        marker=dict(size=4, color=_BAR_COLOR),
        fill="tozeroy",
        fillcolor="rgba(79,142,247,0.08)",
        hovertemplate="%{x}: %{y} present<extra></extra>",
    ))
    fig.update_layout(**_LAYOUT, height=240)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})