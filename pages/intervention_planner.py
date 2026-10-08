import pandas as pd
import streamlit as st

from components.charts import render_bar_chart
from utils.scoring import calculate_priority_score


def _score_frame(catalog: pd.DataFrame):
    if catalog is None or catalog.empty:
        return pd.DataFrame(columns=["area", "priority_score", "contributing_indicators"])
    pivot = catalog.pivot_table(index="area", columns="indicator", values="value", aggfunc="mean").reset_index()
    score_frame = pivot.rename(columns=lambda x: str(x).lower().replace(" ", "_").replace("-", "_"))
    return score_frame


def render_intervention_planner():
    st.title("Intervention Priority Engine")
    st.caption("A practical, explainable prioritization layer using validated poverty indicators only.")

    context = st.session_state.get("dataset_context")
    if context is None:
        st.info("Upload a workbook or load the official NISR dataset to generate intervention priorities.")
        return

    from utils.data_processor import build_indicator_catalog, validate_numeric_table

    catalog = validate_numeric_table(build_indicator_catalog(context["workbook"]))
    if catalog is None or catalog.empty:
        st.warning("The loaded workbook does not contain validated numeric observations that can support a priority score.")
        return

    weights = {}
    default_weights = {
        "poverty_rate": 0.4,
        "food_insecurity": 0.2,
        "consumption_gap": 0.2,
        "vulnerability_index": 0.1,
        "income_gap": 0.1,
    }
    for key, default in default_weights.items():
        weights[key] = st.slider(f"{key.replace('_', ' ').title()} weight", 0.0, 1.0, default)

    score_frame = _score_frame(catalog)
    score_df = calculate_priority_score(score_frame, weights=weights)
    if score_df.empty:
        st.warning("No valid score inputs are available after normalization.")
        return

    st.subheader("Priority ranking")
    render_bar_chart(score_df.head(10), x_col="area", y_col="priority_score", title="Community priority score")
    st.dataframe(score_df.head(20), use_container_width=True)

    st.subheader("How scores are computed")
    st.markdown(
        """
        The engine normalizes comparable indicators and assigns weights chosen by the user. It then ranks each area based on the weighted combination of validated poverty and vulnerability signals.
        This output is a decision-support proxy for intervention prioritization and should be reviewed with local context before designing programs.
        """
    )

    st.subheader("Recommended intervention categories")
    for _, row in score_df.head(5).iterrows():
        st.markdown(
            f"""
            <div class="recommendation-box">
                <strong>{row['area']}</strong> · Priority score {row['priority_score']:.1f}<br>
                Suggested action: financial literacy outreach, savings group support, or mobile money access investigation in the highest-risk communities.
            </div>
            """,
            unsafe_allow_html=True,
        )
