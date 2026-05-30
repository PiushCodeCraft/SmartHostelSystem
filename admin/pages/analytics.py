import streamlit as st
from datetime import datetime
from admin.components.cards import stat_card
from admin.components.charts import (
    monthly_attendance_chart,
    hourly_entry_chart,
    attendance_line_chart,
)
from database.database import (
    get_analytics_summary,
    get_monthly_attendance,
    get_hourly_entry_today,
    get_30day_trend,
)


def show_analytics():
    st.markdown(
        "<h1 style='margin-bottom:1.2rem'>📈 Analytics</h1>",
        unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # FETCH DATA FROM DATABASE
    # ---------------------------------------------------

    summary       = get_analytics_summary()
    monthly_data  = get_monthly_attendance(datetime.now().year)
    hourly_data   = get_hourly_entry_today()
    trend_data    = get_30day_trend()

    avg_daily  = summary.get("avg_daily", 0)
    peak_day   = summary.get("peak_day",  "N/A")
    alerts     = summary.get("alerts",    0)

    # ---------------------------------------------------
    # SUMMARY CARDS
    # ---------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:
        stat_card(
            "📅 Avg Daily Attendance",
            str(avg_daily),
            "Last 30 days"
        )

    with c2:
        stat_card(
            "📆 Peak Day",
            peak_day,
            "Highest attendance day",
            "#3ecf8e"
        )

    with c3:
        stat_card(
            "⚠️ Alerts This Month",
            str(alerts),
            "WARN + ERROR log entries",
            "#f5a623"
        )

    st.markdown(
        "<div style='margin:.9rem 0'></div>",
        unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # CHARTS ROW
    # ---------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style='font-size:.85rem;font-weight:600;
                        color:#e8eaf0;margin-bottom:.4rem'>
                Monthly Attendance
                <span style='font-size:.72rem;color:#7a82a0;font-weight:400'>
                    &mdash; {year}
                </span>
            </div>
            """.format(year=datetime.now().year),
            unsafe_allow_html=True
        )
        monthly_attendance_chart(monthly_data)

    with col2:
        st.markdown(
            """
            <div style='font-size:.85rem;font-weight:600;
                        color:#e8eaf0;margin-bottom:.4rem'>
                Entry by Hour
                <span style='font-size:.72rem;color:#7a82a0;font-weight:400'>
                    &mdash; Today
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
        hourly_entry_chart(hourly_data)

    st.markdown(
        "<div style='margin:.8rem 0'></div>",
        unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # 30-DAY TREND
    # ---------------------------------------------------

    st.markdown(
        """
        <div style='font-size:.85rem;font-weight:600;
                    color:#e8eaf0;margin-bottom:.4rem'>
            30-Day Attendance Trend
        </div>
        """,
        unsafe_allow_html=True
    )
    attendance_line_chart(trend_data)

    # ---------------------------------------------------
    # INSIGHT CALLOUTS
    # ---------------------------------------------------

    st.markdown(
        "<div style='margin:.9rem 0'></div>",
        unsafe_allow_html=True
    )

    i1, i2 = st.columns(2)

    with i1:
        st.markdown(
            f"""
            <div style='background:rgba(79,142,247,.08);
                        border:1px solid rgba(79,142,247,.25);
                        border-radius:10px;padding:.9rem 1rem'>
                <div style='font-size:.8rem;font-weight:600;
                            color:#4f8ef7;margin-bottom:.3rem'>
                    💡 Insight
                </div>
                <div style='font-size:.82rem;color:#e8eaf0'>
                    Peak attendance day is <strong>{peak_day}</strong>.
                    Average daily presence over the last 30 days is
                    <strong>{avg_daily} students</strong>.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with i2:
        st.markdown(
            f"""
            <div style='background:rgba(245,166,35,.08);
                        border:1px solid rgba(245,166,35,.25);
                        border-radius:10px;padding:.9rem 1rem'>
                <div style='font-size:.8rem;font-weight:600;
                            color:#f5a623;margin-bottom:.3rem'>
                    ⚠️ Alert Trend
                </div>
                <div style='font-size:.82rem;color:#e8eaf0'>
                    <strong>{alerts} security alerts</strong> (WARN/ERROR)
                    recorded in the last 30 days. Review live logs for details.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )