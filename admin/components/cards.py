import streamlit as st
import textwrap

def _render_html(content: str):
    st.markdown(textwrap.dedent(content).strip(), unsafe_allow_html=True)


def stat_card(label: str, value: str, sub: str = "", color: str = "#e8eaf0"):
    """Render a single metric stat card with custom HTML."""
    _render_html(f"""
    <div style='background:#181c27;border:1px solid #2a2f45;border-radius:12px;padding:1rem 1.1rem'>
        <div style='font-size:.75rem;color:#7a82a0;margin-bottom:.4rem'>{label}</div>
        <div style='font-size:1.6rem;font-weight:700;color:{color}'>{value}</div>
        <div style='font-size:.72rem;color:#7a82a0;margin-top:.2rem'>{sub}</div>
    </div>
    """)


def progress_row(label: str, pct: int, color: str = "#4f8ef7"):
    """Render a labelled progress bar row."""
    _render_html(f"""
    <div style='margin-bottom:.7rem'>
        <div style='display:flex;justify-content:space-between;font-size:.82rem;margin-bottom:.3rem'>
            <span style='color:#7a82a0'>{label}</span>
            <span style='color:#e8eaf0'>{pct}%</span>
        </div>
        <div style='height:5px;background:#1e2233;border-radius:3px;overflow:hidden'>
            <div style='height:100%;width:{pct}%;background:{color};border-radius:3px'></div>
        </div>
    </div>
    """)


def section_header(title: str, subtitle: str = ""):
    _render_html(f"""
    <div style='margin-bottom:1rem'>
        <h3 style='font-size:1rem;font-weight:600;color:#e8eaf0;margin:0'>{title}</h3>
        {f'<p style="font-size:.8rem;color:#7a82a0;margin:2px 0 0">{subtitle}</p>' if subtitle else ''}
    </div>
    """)
