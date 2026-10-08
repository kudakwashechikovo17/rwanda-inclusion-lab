import io
import re
import requests
import pandas as pd
import streamlit as st

DATA_URL = "https://statistics.gov.rw/sites/default/files/documents/2025-05/EICV7_Tables_Rwanda_Poverty_Profile.xlsx"
st.set_page_config(page_title="Rwanda Inclusion Lab", page_icon="🇷🇼", layout="wide")
st.title("🇷🇼 Rwanda Inclusion Lab")
st.caption("EICV7 poverty evidence explorer • NISR 2025 • Hackathon Track 2")
st.info("Important: Poverty is not the same as financial exclusion. This workbook can describe poverty patterns, but cannot establish who lacks a bank account, mobile money, or credit. Combine with a financial-access dataset for direct exclusion estimates.")

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_workbook():
    response = requests.get(DATA_URL, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return response.content

upload = st.sidebar.file_uploader("Upload EICV7 workbook (.xlsx)", type=["xlsx"])
if upload:
    contents = upload.getvalue()
else:
    try:
        with st.spinner("Downloading official EICV7 tables..."):
            contents = fetch_workbook()
    except Exception as exc:
        st.error("Could not download the workbook. Download it from NISR and upload it in the sidebar.")
        st.caption(f"Connection details: {exc}")
        st.stop()

try:
    book = pd.ExcelFile(io.BytesIO(contents), engine="openpyxl")
except Exception as exc:
    st.error(f"Unable to read the Excel workbook: {exc}")
    st.stop()

st.sidebar.success(f"{len(book.sheet_names)} worksheets loaded")
query = st.sidebar.text_input("Find relevant worksheets", "poverty")
matches = [s for s in book.sheet_names if query.lower() in s.lower()] if query else book.sheet_names
sheet = st.sidebar.selectbox("Worksheet", matches or book.sheet_names)
raw = pd.read_excel(book, sheet_name=sheet, header=None)
st.subheader(f"Worksheet: {sheet}")
st.caption("Displayed values come directly from the workbook; titles and footnotes may occupy rows.")
st.dataframe(raw.fillna(""), use_container_width=True, height=440)

st.subheader("Explore figures")
row_number = st.number_input("Header row (1-based; change if the sheet has title rows)", min_value=1, max_value=max(1,len(raw)), value=1)
header = raw.iloc[row_number-1].astype(str).tolist()
data = raw.iloc[row_number:].copy()
data.columns = [f"{name} ({i+1})" if header.count(name)>1 else name for i,name in enumerate(header)]
data = data.dropna(how="all")
cols = list(data.columns)
if len(cols) >= 2:
    label_col = st.selectbox("Category / area column", cols)
    metric_col = st.selectbox("Value column", cols, index=1)
    chart = pd.DataFrame({"Category": data[label_col].astype(str), "Value": pd.to_numeric(data[metric_col], errors="coerce")}).dropna()
    chart = chart[~chart["Category"].str.lower().isin(["nan", "total"])]
    if len(chart):
        st.bar_chart(chart.head(30).set_index("Category")["Value"])
        st.download_button("Download selected values (CSV)", chart.to_csv(index=False).encode(), "selected_eicv7.csv", "text/csv")
    else:
        st.warning("No numeric values found for this column selection. Choose another row or column.")

st.subheader("Find poverty-related evidence")
keywords = st.text_input("Search cells", "poverty")
if keywords.strip():
    found = []
    for name in book.sheet_names:
        frame = pd.read_excel(book, sheet_name=name, header=None, dtype=str)
        mask = frame.fillna("").apply(lambda col: col.str.contains(re.escape(keywords), case=False, regex=True)).any(axis=1)
        for idx in frame.index[mask][:15]:
            found.append({"Sheet": name, "Excel row": int(idx)+1, "Matching row": " | ".join(frame.loc[idx].fillna("").astype(str).tolist())[:300]})
    if found:
        st.dataframe(pd.DataFrame(found), use_container_width=True)
    else:
        st.info("No matching rows in the workbook.")

st.subheader("How this answers Track 2")
st.markdown("""
**Question:** Where are poverty-related vulnerabilities concentrated, and where might financial-inclusion programs prioritize further investigation?

**Approach:** Explore EICV7 poverty tables by geography and population group, compare reported values, and flag high-poverty areas for follow-up. This is a **prioritization proxy**, not a measured financial-exclusion rate.

**For a direct financial-exclusion answer:** Join appropriately matched NISR/FinScope financial-access indicators (banking, mobile money, credit, savings) to the same geographic or demographic level. Never infer individual financial status from aggregated poverty rates.

**Limitations:** Workbook tables can use different units and denominators. Check the source table headings and footnotes before comparing or interpreting values.
""")
st.markdown(f"[Official EICV7 workbook]({DATA_URL}) · Source: National Institute of Statistics of Rwanda (NISR)")
