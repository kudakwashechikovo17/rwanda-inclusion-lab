import re

import numpy as np
import pandas as pd


NON_DATA_TOKENS = {
    "table",
    "title",
    "notes",
    "footnote",
    "source",
    "definition",
    "indicator",
    "unit",
    "rwanda poverty",
    "poverty profile",
}


def _clean_cell(value):
    if value is None or pd.isna(value):
        return ""
    text = str(value).strip()
    return re.sub(r"\s+", " ", text)


def _to_float(value):
    if value is None or pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "").replace("%", "")
    if not text or text.lower() in {"nan", "n/a", "na"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def infer_area_type(value: str) -> str:
    text = (value or "").lower()
    if any(k in text for k in ["urban", "rural"]):
        return "residence"
    if any(k in text for k in ["male", "female", "sex", "gender"]):
        return "demographic"
    if any(k in text for k in ["province", "district", "city", "sector", "village"]):
        return "geography"
    return "group"


def normalize_indicator_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Convert a raw worksheet into a clean indicator table with area/value rows."""
    if raw_df is None or raw_df.empty:
        return pd.DataFrame(columns=["sheet", "area", "indicator", "value", "unit", "area_type", "year"])

    df = raw_df.copy()
    df = df.map(_clean_cell)
    df = df.replace({"": np.nan})
    df = df.dropna(how="all")
    if df.empty:
        return pd.DataFrame(columns=["sheet", "area", "indicator", "value", "unit", "area_type", "year"])

    header_index = 0
    for idx in range(min(len(df), 15)):
        row = df.iloc[idx].fillna("").astype(str)
        row_text = " ".join(row.tolist()).lower()
        if any(keyword in row_text for keyword in ["province", "district", "urban", "rural", "poverty", "rate", "area", "value"]):
            header_index = idx
            break

    headers = []
    seen = {}
    for i, value in enumerate(df.iloc[header_index].tolist()):
        label = _clean_cell(value) or f"column_{i + 1}"
        label = re.sub(r"\s+", " ", label)
        base = label
        seen[base] = seen.get(base, 0) + 1
        if seen[base] > 1:
            label = f"{label}_{seen[base]}"
        headers.append(label)

    normalized = df.iloc[header_index + 1 :].copy()
    if normalized.empty:
        return pd.DataFrame(columns=["sheet", "area", "indicator", "value", "unit", "area_type", "year"])

    normalized.columns = headers[: normalized.shape[1]]
    result_rows = []

    for _, row in normalized.iterrows():
        row_values = row.to_dict()
        area = ""
        numeric_cells = []

        for column, value in row_values.items():
            cleaned = _clean_cell(value)
            if not cleaned:
                continue
            numeric = _to_float(value)
            if numeric is not None:
                numeric_cells.append((column, numeric))
            elif area == "":
                area = cleaned

        if not area:
            for column, value in row_values.items():
                if column.lower().startswith("column_"):
                    continue
                if not _clean_cell(value):
                    continue
                area = _clean_cell(value)
                break

        if not area:
            continue

        for column, numeric_value in numeric_cells:
            if column.lower() in {"sheet", "area", "indicator", "year"}:
                continue
            area_name = area
            if any(token in area_name.lower() for token in ["total", "all", "national", "rwanda"]) and any(token in column.lower() for token in ["area", "province", "district"]):
                continue
            result_rows.append({
                "area": area_name,
                "indicator": column,
                "value": numeric_value,
                "unit": "",
                "area_type": infer_area_type(area_name),
                "year": None,
            })

    if not result_rows:
        return pd.DataFrame(columns=["sheet", "area", "indicator", "value", "unit", "area_type", "year"])

    cleaned = pd.DataFrame(result_rows)
    cleaned = cleaned[cleaned["area"].astype(str).str.strip() != ""].copy()
    cleaned["value"] = pd.to_numeric(cleaned["value"], errors="coerce")
    cleaned = cleaned.dropna(subset=["value"]).copy()
    cleaned = cleaned.drop_duplicates(subset=["area", "indicator", "value"], keep="first")
    return cleaned


def validate_numeric_table(frame: pd.DataFrame) -> pd.DataFrame | None:
    """Return a cleaned table with only rows that contain useful numeric values."""
    if frame is None or frame.empty:
        return None
    data = frame.copy()
    if "value" not in data.columns:
        return None
    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    data = data.dropna(subset=["value"]).copy()
    data = data[data["area"].fillna("").astype(str).str.strip() != ""]
    return data


def find_relevant_sheets(book) -> list[str]:
    candidates = []
    for sheet_name in book.sheet_names:
        lowered = sheet_name.lower()
        if any(keyword in lowered for keyword in ["poverty", "vulnerability", "demographic", "household", "income", "consumption", "material"]):
            candidates.append(sheet_name)
    return candidates or book.sheet_names[:5]


def build_indicator_catalog(workbook) -> pd.DataFrame:
    rows = []
    for sheet_name in workbook.sheet_names:
        try:
            frame = pd.read_excel(workbook, sheet_name=sheet_name, header=None)
        except Exception:
            continue
        normalized = normalize_indicator_dataframe(frame)
        if normalized.empty:
            continue
        normalized.insert(0, "sheet", sheet_name)
        rows.append(normalized)

    if not rows:
        return pd.DataFrame(columns=["sheet", "area", "indicator", "value", "unit", "area_type", "year"])

    return pd.concat(rows, ignore_index=True)
