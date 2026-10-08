import pandas as pd
import streamlit as st

from components.charts import render_bar_chart
from utils.data_processor import build_indicator_catalog, validate_numeric_table


def render_poverty_explorer():
    st.title("Poverty Explorer")
    st.caption("Filter, compare, and export validated poverty indicators from the NISR workbook.")

    context = st.session_state.get("dataset_context")
    if context is None:
        st.info("No dataset is currently loaded. Upload a workbook or load the official NISR dataset from the sidebar.")
        return

    catalog = validate_numeric_table(build_indicator_catalog(context["workbook"]))
    if catalog is None or catalog.empty:
        st.warning("No numeric indicator rows could be validated from the workbook.")
        return

    area_options = sorted(catalog["area"].dropna().astype(str).unique().tolist())
    indicator_options = sorted(catalog["indicator"].dropna().astype(str).unique().tolist())

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_area = st.selectbox("Province or district", ["All"] + area_options, index=0)
    with col2:
        selected_indicator = st.selectbox("Poverty indicator", ["All"] + indicator_options, index=0)
    with col3:
        selected_year = st.selectbox("Year", ["All"] + sorted({str(year) for year in catalog["year"].dropna().astype(str).unique().tolist()}), index=0)

    filtered = catalog.copy()
    if selected_area != "All":
        filtered = filtered[filtered["area"].astype(str).str.contains(selected_area, case=False, na=False)]
    if selected_indicator != "All":
        filtered = filtered[filtered["indicator"].astype(str).str.contains(selected_indicator, case=False, na=False)]
    if selected_year != "All":
        filtered = filtered[filtered["year"].astype(str).str.contains(selected_year, case=False, na=False)]

    if filtered.empty:
        st.warning("No rows match the chosen filters. Try another indicator or area filter.")
        return

    summary = filtered.groupby("area", as_index=False)["value"].mean().sort_values("value", ascending=False)
    summary.columns = ["area", "value"]
    render_bar_chart(summary.head(15), x_col="area", y_col="value", title=f"Comparison: {selected_indicator if selected_indicator != 'All' else 'selected poverty indicators'}")

    st.subheader("Validated observations")
    st.dataframe(filtered.sort_values("value", ascending=False).reset_index(drop=True), use_container_width=True)

    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV export", csv_data, file_name="imibereho_poverty_export.csv", mime="text/csv")
