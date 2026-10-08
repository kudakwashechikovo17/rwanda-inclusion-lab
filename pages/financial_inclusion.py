import pandas as pd
import streamlit as st

from components.charts import render_bar_chart
from utils.data_processor import build_indicator_catalog, validate_numeric_table
from utils.insights import generate_insights


def render_financial_inclusion():
    st.title("Financial Inclusion Intelligence")
    st.caption("Poverty vulnerability data is a prioritization proxy, not a direct measure of financial exclusion.")

    context = st.session_state.get("dataset_context")
    if context is None:
        st.info("Load the dataset to review poverty-based prioritization signals for financial inclusion interventions.")
        return

    catalog = validate_numeric_table(build_indicator_catalog(context["workbook"]))
    if catalog is None or catalog.empty:
        st.warning("No validated poverty indicators are available for financial inclusion prioritization.")
        return

    st.info("This view highlights where poverty vulnerability can justify deeper investigation into financial products and support programs. It does not assert that any individual is financially excluded based on poverty alone.")

    area_summary = catalog.groupby("area", as_index=False)["value"].mean().sort_values("value", ascending=False).head(10)
    render_bar_chart(area_summary, x_col="area", y_col="value", title="Geographic disparity in poverty-linked vulnerability")

    insights = generate_insights(catalog, max_insights=4)
    st.subheader("Priority intervention areas")
    for insight in insights:
        st.markdown(
            f"""
            <div class="recommendation-box">
                <strong>{insight['indicator']}</strong><br>
                {insight['text']}<br>
                <small>Evidence: {insight['evidence']}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    recommended_interventions = [
        "Financial literacy programs for vulnerable households",
        "Savings group support in high-poverty community clusters",
        "Mobile money access investigation in underserved areas",
        "Affordable credit assessment for low-income households",
        "Social protection referrals linked to local service providers",
    ]
    st.subheader("Potential intervention categories")
    for item in recommended_interventions:
        st.markdown(f"- {item}")

    st.subheader("Available socioeconomic indicators")
    indicator_frame = pd.DataFrame({"Indicator": sorted(catalog["indicator"].dropna().astype(str).unique())})
    st.dataframe(indicator_frame, use_container_width=True)
