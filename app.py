import streamlit as st

from components.sidebar import render_sidebar
from pages.community_comparison import render_community_comparison
from pages.dashboard import render_dashboard
from pages.financial_inclusion import render_financial_inclusion
from pages.intervention_planner import render_intervention_planner
from pages.methodology import render_methodology
from pages.poverty_explorer import render_poverty_explorer

st.set_page_config(page_title="IMIBEREHO", page_icon="🇷🇼", layout="wide")

st.markdown(
    """
    <style>
        :root {
            --primary: #0B2545;
            --secondary: #13315C;
            --accent: #00C896;
            --bg: #F5F7FB;
            --card: #FFFFFF;
            --text: #1F2937;
        }
        .stApp {
            background: var(--bg);
            color: var(--text);
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
        }
        .brand-box {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 18px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .brand-mark {
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            color: #FFFFFF;
        }
        .brand-subtitle {
            font-size: 0.76rem;
            color: rgba(255,255,255,0.8);
            margin-top: 0.45rem;
        }
        .metric-card {
            background: var(--card);
            border-radius: 18px;
            padding: 1rem 1.2rem;
            box-shadow: 0 12px 30px rgba(11, 37, 69, 0.08);
            margin-bottom: 1rem;
        }
        .metric-title {
            color: #6B7280;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.3rem;
        }
        .metric-value {
            color: var(--primary);
            font-size: 2rem;
            font-weight: 700;
            line-height: 1.2;
        }
        .metric-subtitle {
            color: #6B7280;
            font-size: 0.8rem;
            margin-top: 0.35rem;
        }
        .section-title {
            color: var(--primary);
            font-size: 1.2rem;
            font-weight: 700;
            margin-top: 0.8rem;
            margin-bottom: 0.2rem;
        }
        .insight-box {
            background: white;
            padding: 0.85rem 1rem;
            border-left: 4px solid var(--accent);
            border-radius: 12px;
            margin-bottom: 0.5rem;
        }
        .recommendation-box {
            background: linear-gradient(135deg, rgba(0,200,150,0.08), rgba(11,37,69,0.04));
            padding: 1rem;
            border-radius: 14px;
            margin-bottom: 0.75rem;
        }
        .stTabs [role="tablist"] {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 12px;
            padding: 0.2rem;
            border: 1px solid rgba(11,37,69,0.08);
        }
        .stTabs [role="tab"] {
            color: var(--primary);
            font-weight: 600;
        }
        .stDownloadButton > button {
            width: 100%;
            background: var(--primary);
            color: white;
            border-radius: 12px;
            border: none;
            font-weight: 600;
        }
        .stButton > button {
            border-radius: 12px;
            background: var(--accent);
            color: var(--primary);
            border: none;
            font-weight: 700;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

render_sidebar()

pages = [
    st.Page(render_dashboard, title="Executive Dashboard", icon="📊"),
    st.Page(render_poverty_explorer, title="Poverty Explorer", icon="🔎"),
    st.Page(render_financial_inclusion, title="Financial Inclusion Intelligence", icon="💳"),
    st.Page(render_intervention_planner, title="Intervention Priority Engine", icon="🎯"),
    st.Page(render_community_comparison, title="Community Comparison", icon="📈"),
    st.Page(render_methodology, title="Data & Methodology", icon="🧭"),
]

page = st.navigation(pages, position="sidebar")
page.run()
