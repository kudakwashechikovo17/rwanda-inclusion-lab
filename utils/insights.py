import pandas as pd


def generate_insights(catalog: pd.DataFrame, max_insights: int = 5):
    """Generate rule-based insights that reference actual values and the indicator name."""
    if catalog is None or catalog.empty:
        return [
            {
                "text": "No validated poverty indicators are available yet. Load the official NISR workbook or upload a dataset to generate evidence-backed insights.",
                "evidence": "No dataset loaded",
                "indicator": "n/a",
            }
        ]

    data = catalog.copy()
    if "value" not in data.columns:
        return [{"text": "The workbook does not include usable numeric poverty observations.", "evidence": "No numeric values", "indicator": "n/a"}]

    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    data = data.dropna(subset=["value"]).copy()
    insights = []

    if data.empty:
        return [{"text": "The loaded workbook has no validated observations after data cleaning.", "evidence": "Empty dataset", "indicator": "n/a"}]

    area_bands = data.groupby("area", as_index=False)["value"].mean().sort_values("value", ascending=False)
    if len(area_bands) > 1:
        highest_area = area_bands.iloc[0]
        lowest_area = area_bands.iloc[-1]
        # pick indicator with the strongest spread in the selected table
        indicator = data.groupby("indicator")["value"].mean().idxmax()
        insights.append(
            {
                "text": f"{highest_area['area']} reports a higher mean {indicator} than {lowest_area['area']}.",
                "evidence": f"{highest_area['area']} = {highest_area['value']:.2f}; {lowest_area['area']} = {lowest_area['value']:.2f}",
                "indicator": indicator,
            }
        )

    grouped = data.groupby("indicator", as_index=False)["value"].mean().sort_values("value", ascending=False)
    for _, row in grouped.head(max_insights).iterrows():
        if any(item["indicator"] == row["indicator"] for item in insights):
            continue
        insights.append(
            {
                "text": f"The indicator {row['indicator']} is among the strongest observed measures in the current dataset.",
                "evidence": f"Mean value = {row['value']:.2f}",
                "indicator": row["indicator"],
            }
        )

    return insights[:max_insights]
