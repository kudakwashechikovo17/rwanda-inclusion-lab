import streamlit as st


def metric_card(title: str, value: str, subtitle: str = "", accent: str = "#00C896"):
    st.markdown(
        f"""
        <div class="metric-card" style="border-left: 5px solid {accent};">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_heading(title: str, subtitle: str = ""):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)
