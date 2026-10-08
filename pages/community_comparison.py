import pandas as pd
import streamlit as st

from components.charts import render_bar_chart
from utils.data_processor import build_indicator_catalog, validate_numeric_table


def render_community_comparison():
    st.title("Community Comparison")
    st.caption("Compare vulnerability patterns across geographic and demographic groups.")

    context = st.session_state.get("dataset_context")
    if context is None:
        st.info("Load the dataset to compare communities and vulnerability indicators.")
        return

    catalog = validate_numeric_table(build_indicator_catalog(context["workbook"]))
    if catalog is None or catalog.empty:
        st.warning("No comparable community data is available in the current workbook.")
        return

    areas = sorted(catalog["area"].dropna().astype(str).unique().tolist())
    col1, col2 = st.columns(2)
    with col1:
        area_a = st.selectbox("Area A", areas, index=0 if areas else 0)
    with col2:
        area_b = st.selectbox("Area B", areas, index=min(1, len(areas)-1) if len(areas) > 1 else 0)

    comparison = catalog[catalog["area"].astype(str).isin([area_a, area_b])]
    if comparison.empty:
        st.info("No matching community observations were found.")
        return

    pivoted = comparison.pivot_table(index="indicator", columns="area", values="value", aggfunc="mean").reset_index()
    if pivoted.empty:
        st.warning("The selected areas do not share valid numeric indicators.")
        return

    pivoted["difference"] = (pivoted[area_a] - pivoted[area_b]).fillna(0)
    st.subheader("Indicator differences")
    st.dataframe(pivoted.sort_values("difference", ascending=False), use_container_width=True)

    bar_df = pivoted[ ["indicator", area_a, area_b] ].sort_values(area_a, ascending=False).head(12)
    render_bar_chart(bar_df.melt(id_vars=["indicator"], var_name="Area", value_name="Value"), x_col="indicator", y_col="Value", title="Side-by-side comparison")

    st.subheader("Vulnerability summary")
    summary = comparison.groupby("area", as_index=False)["value"].mean().sort_values("value", ascending=False)
    st.bar_chart(summary.set_index("area")["value"])
