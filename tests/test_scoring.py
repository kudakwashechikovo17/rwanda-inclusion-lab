import pandas as pd

from utils.scoring import calculate_priority_score


def test_calculate_priority_score_uses_available_weights():
    scores = pd.DataFrame(
        {
            "area": ["Kigali", "Western"],
            "poverty_rate": [34.2, 26.5],
            "food_insecurity": [18.0, 14.5],
            "urban_rural_gap": [12.0, 8.5],
        }
    )

    result = calculate_priority_score(scores, weights={"poverty_rate": 0.5, "food_insecurity": 0.3})

    assert "priority_score" in result.columns
    assert result["priority_score"].notna().all()
    assert result.loc[result["area"] == "Kigali", "priority_score"].iloc[0] > result.loc[result["area"] == "Western", "priority_score"].iloc[0]
