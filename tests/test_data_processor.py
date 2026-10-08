import pandas as pd

from utils.data_processor import normalize_indicator_dataframe, validate_numeric_table


def test_normalize_indicator_dataframe_extracts_numeric_rows():
    df = pd.DataFrame(
        [
            ["Table 1", "Poverty rate", "Province", "Value"],
            ["Kigali City", "", 25.4, ""],
            ["Western", "", 26.2, ""],
            ["Total", "", 27.5, ""],
        ]
    )

    normalized = normalize_indicator_dataframe(df)

    assert not normalized.empty
    assert "area" in normalized.columns
    assert "value" in normalized.columns
    assert normalized["value"].dtype.kind in "ifuf"
    assert normalized["area"].tolist() == ["Kigali City", "Western"]


def test_validate_numeric_table_rejects_missing_values():
    data = pd.DataFrame({"area": ["Kigali", "Ruhango"], "value": [12.5, None]})

    result = validate_numeric_table(data)

    assert result is not None
    assert list(result["area"]) == ["Kigali"]
