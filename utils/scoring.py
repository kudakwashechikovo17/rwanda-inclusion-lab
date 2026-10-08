import pandas as pd


DEFAULT_WEIGHTS = {
    "poverty_rate": 0.35,
    "food_insecurity": 0.2,
    "consumption_gap": 0.15,
    "vulnerability_index": 0.15,
    "income_gap": 0.15,
}


def calculate_priority_score(frame: pd.DataFrame, weights=None) -> pd.DataFrame:
    """Score areas based on poverty vulnerability indicators while remaining explainable."""
    if frame is None or frame.empty:
        return pd.DataFrame(columns=["area", "priority_score", "contributing_indicators"])

    data = frame.copy()
    if "area" not in data.columns:
        return data.copy()

    data["area"] = data["area"].astype(str).fillna("")
    data = data[data["area"].str.strip() != ""].copy()

    selected_weights = dict(DEFAULT_WEIGHTS)
    if weights:
        selected_weights.update({key: float(value) for key, value in weights.items() if value is not None})

    available = [column for column in data.columns if column != "area" and column in selected_weights]
    if not available:
        available = [column for column in data.columns if column != "area"]

    normalized = []
    for column in available:
        series = pd.to_numeric(data[column], errors="coerce")
        if series.notna().any():
            normalized.append(series.rank(pct=True, method="average"))

    if not normalized:
        result = data[["area"]].copy()
        result["priority_score"] = 0.0
        result["contributing_indicators"] = "No valid indicators available"
        return result

    score = sum(n * selected_weights.get(column, 1 / len(available)) for n, column in zip(normalized, available))
    result = data[["area"]].copy()
    result["priority_score"] = (score / len(normalized)) * 100
    result["contributing_indicators"] = ", ".join(available)
    return result.sort_values("priority_score", ascending=False).reset_index(drop=True)
