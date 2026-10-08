import pandas as pd
import streamlit as st

from components.cards import metric_card
from components.charts import render_bar_chart
from utils.data_processor import build_indicator_catalog, validate_numeric_table
from utils.insights import generate_insights


def _catalog_for_dashboard():
    context = st.session_state.get("dataset_context")
    if context is None:
        return pd.DataFrame(columns=["sheet", "area", "indicator", "value", "unit", "area_type", "year"])
    return build_indicator_catalog(context["workbook"])


def _find_metric(data: pd.DataFrame, hint_keywords: list[str]):
    if data.empty:
        return None
    rows = data.copy()
    rows["indicator_lower"] = rows["indicator"].fillna("").astype(str).str.lower()
    match = rows[rows["indicator_lower"].str.contains("|".join(hint_keywords), case=False, na=False)]
    if match.empty:
        return None
    return match.sort_values("value", ascending=False).reset_index(drop=True)


def render_dashboard():
    st.title("IMIBEREHO Executive Dashboard")
    st.caption("Rwanda Financial Inclusion & Poverty Intelligence Platform")

    context = st.session_state.get("dataset_context")
    if context is None:
        st.info("Load the official NISR dataset or upload an Excel file to unlock the dashboard.")
        return

    catalog = validate_numeric_table(_catalog_for_dashboard())
    if catalog is None or catalog.empty:
        st.warning("The loaded workbook did not contain validated numeric observations after cleaning. Try a different worksheet or upload a fresh Excel file.")
        return

    st.markdown("<div class='section-title'>National overview</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    national_match = catalog[catalog["area"].astype(str).str.lower().str.contains("rwanda|national|total", na=False)]
    poverty_metric = _find_metric(national_match, ["poverty", "poverty rate", "poor", "population below poverty"])
    extreme_metric = _find_metric(national_match, ["extreme poverty", "extreme", "food poverty", "poverty line"])
    available_indicators = sorted(catalog["indicator"].dropna().unique().tolist())

    with col1:
        value = poverty_metric["value"].mean() if poverty_metric is not None and not poverty_metric.empty else None
        metric_card("National poverty rate", f"{value:.2f}%" if value is not None else "N/A", "Validated against the loaded workbook")
    with col2:
        value = extreme_metric["value"].mean() if extreme_metric is not None and not extreme_metric.empty else None
        metric_card("Extreme poverty rate", f"{value:.2f}%" if value is not None else "N/A", "Validated against the loaded workbook")
    with col3:
        metric_card("Available comparison indicators", str(len(available_indicators)), "Distinct poverty indicators in the dataset")
    with col4:
        highest_area = catalog.groupby("area")["value"].mean().sort_values(ascending=False).head(1)
        highest_value = highest_area.iloc[0] if not highest_area.empty else None
        metric_card("Highest observed area", f"{highest_area.index[0] if highest_area.index.size else 'N/A'}", f"Mean value: {highest_value:.2f}" if highest_value is not None else "No comparable area values")

    st.markdown("---")

    st.markdown("<div class='section-title'>Regional comparisons</div>", unsafe_allow_html=True)
    comparison = catalog.groupby("area", as_index=False)["value"].mean().sort_values("value", ascending=False).head(10)
    comparison.columns = ["area", "value"]
    render_bar_chart(comparison, x_col="area", y_col="value", title="Top poverty and vulnerability scores by area")

    st.markdown("---")

    st.markdown("<div class='section-title'>Key insights</div>", unsafe_allow_html=True)
    insights = generate_insights(catalog, max_insights=5)
    for insight in insights:
        st.markdown(
            f"""
            <div class="insight-box">
                <strong>{insight['indicator']}</strong><br>
                {insight['text']}<br>
                <small>Evidence: {insight['evidence']}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("<div class='section-title'>Policy recommendations</div>", unsafe_allow_html=True)
    recommendations = [
        "Prioritize districts and communities with the highest validated poverty vulnerability scores for targeted financial literacy and savings support.",
        "Investigate mobile money and affordability constraints in the most vulnerable rural and peri-urban areas before scaling loan products.",
        "Combine poverty vulnerability signals with social protection referrals and local outreach programs to improve inclusion pathways.",
    ]
    for recommendation in recommendations:
        st.markdown(f"<div class='recommendation-box'>{recommendation}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Available poverty comparison indicators")
    st.dataframe(pd.DataFrame({"Indicator": available_indicators[:20]}), use_container_width=True)
