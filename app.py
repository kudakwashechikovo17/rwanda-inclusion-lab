import streamlit as st

from components.sidebar import render_sidebar
from pages.community_comparison import render_community_comparison
from pages.dashboard import render_dashboard
from pages.financial_inclusion import render_financial_inclusion
from pages.intervention_planner import render_intervention_planner
from pages.methodology import render_methodology
from pages.poverty_explorer import render_poverty_explorer

st.set_page_config(page_title="IMIBEREHO", page_icon=":material/insights:", layout="wide")

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
            background: #101019;
            color: #F4F4F7;
        }
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding: 1.35rem 1rem 1rem;
        }
        [data-testid="stSidebar"] h3 {
            color: #FFFFFF;
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 0.15rem;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #AAAAB6;
            font-size: 0.82rem;
        }
        [data-testid="stSidebar"] [data-testid="stTextInput"] input {
            background: #383842;
            color: #FFFFFF;
            border: 1px solid #45454F;
            border-radius: 7px;
            min-height: 2.65rem;
        }
        [data-testid="stSidebar"] [data-testid="stTextInput"] input::placeholder {
            color: #AAAAB6;
        }
        [data-testid="stSidebar"] a[data-testid*="PageLink"] {
            color: #AAAAB6;
            border-radius: 7px;
            min-height: 2.65rem;
            padding: 0.55rem 0.65rem;
            transition: background-color 120ms ease, color 120ms ease;
        }
        [data-testid="stSidebar"] a[data-testid*="PageLink"]:hover {
            color: #FFFFFF;
            background: #24242E;
        }
        [data-testid="stSidebar"] a[data-testid*="PageLink"][aria-current="page"] {
            color: #101019;
            background: #FFFFFF;
            font-weight: 600;
        }
        [data-testid="stSidebar"] a[data-testid*="PageLink"][aria-current="page"] span {
            color: #101019;
        }
        [data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.sidebar-active-marker) + [data-testid="stElementContainer"] a[data-testid="stPageLink-NavLink"] {
            color: #101019;
            background: #FFFFFF;
            font-weight: 600;
        }
        [data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.sidebar-active-marker) + [data-testid="stElementContainer"] a[data-testid="stPageLink-NavLink"] span {
            color: #101019;
        }
        [data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.sidebar-active-marker) + [data-testid="stElementContainer"] a[data-testid="stPageLink-NavLink"] p {
            color: #101019;
        }
        .sidebar-section-label {
            color: #777784;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            margin: 1.15rem 0 0.35rem;
            text-transform: uppercase;
        }
        .sidebar-rule {
            border-top: 1px solid #292933;
            margin: 1rem 0 0.8rem;
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
        [data-testid="stSidebar"] .stButton > button {
            color: #FFFFFF;
        }
        [data-testid="stSidebar"] .stButton > button p {
            color: #FFFFFF !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

page_groups = {
    "OVERVIEW": [
        (st.Page(render_dashboard, title="Executive Dashboard", icon=":material/dashboard:"), ":material/dashboard:"),
    ],
    "EXPLORE": [
        (st.Page(render_poverty_explorer, title="Poverty Explorer", icon=":material/search_insights:"), ":material/search_insights:"),
        (st.Page(render_financial_inclusion, title="Financial Inclusion Intelligence", icon=":material/account_balance:"), ":material/account_balance:"),
    ],
    "PRIORITIZE": [
        (st.Page(render_intervention_planner, title="Intervention Priority Engine", icon=":material/ads_click:"), ":material/ads_click:"),
        (st.Page(render_community_comparison, title="Community Comparison", icon=":material/compare_arrows:"), ":material/compare_arrows:"),
    ],
    "REFERENCE": [
        (st.Page(render_methodology, title="Data & Methodology", icon=":material/menu_book:"), ":material/menu_book:"),
    ],
}

navigation_groups = {
    label: [page_item for page_item, _icon in grouped_pages]
    for label, grouped_pages in page_groups.items()
}
page = st.navigation(navigation_groups, position="hidden")
render_sidebar(page_groups, page.title)
page.run()
