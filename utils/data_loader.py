import io

import pandas as pd
import requests
import streamlit as st

DATA_URL = "https://statistics.gov.rw/sites/default/files/documents/2025-05/EICV7_Tables_Rwanda_Poverty_Profile.xlsx"


@st.cache_data(ttl=3600)
def fetch_official_dataset() -> bytes:
    """Download the official NISR EICV7 workbook and cache the result."""
    response = requests.get(DATA_URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return response.content


def load_workbook_from_bytes(content: bytes):
    return pd.ExcelFile(io.BytesIO(content), engine="openpyxl")


def get_dataset_context(uploaded_file=None):
    """Return a normalized dataset context for the app from an upload or official URL."""
    if uploaded_file is not None:
        payload = uploaded_file.getvalue()
        source = "uploaded"
    else:
        payload = fetch_official_dataset()
        source = "official"

    workbook = load_workbook_from_bytes(payload)
    sheet_summaries = []
    for sheet_name in workbook.sheet_names:
        try:
            frame = pd.read_excel(workbook, sheet_name=sheet_name, header=None)
            sheet_summaries.append({
                "sheet": sheet_name,
                "rows": int(frame.shape[0]),
                "columns": int(frame.shape[1]),
            })
        except Exception:
            sheet_summaries.append({"sheet": sheet_name, "rows": 0, "columns": 0})

    return {
        "source": source,
        "payload": payload,
        "workbook": workbook,
        "sheet_summaries": sheet_summaries,
    }
