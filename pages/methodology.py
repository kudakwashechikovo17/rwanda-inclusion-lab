import streamlit as st


def render_methodology():
    st.title("Data & Methodology")
    st.caption("Transparent documentation for the evidence lifecycle behind IMIBEREHO.")

    st.subheader("Official data source")
    st.markdown("- National Institute of Statistics of Rwanda (NISR)")
    st.markdown("- EICV7 Rwanda Poverty Profile tables")
    st.markdown("- Dataset URL: https://statistics.gov.rw/sites/default/files/documents/2025-05/EICV7_Tables_Rwanda_Poverty_Profile.xlsx")

    st.subheader("Dataset processing methodology")
    st.markdown(
        """
        1. Download the official Excel workbook or accept a user-uploaded fallback.
        2. Read each worksheet and identify the header row by searching for geographic, poverty, and indicator keywords.
        3. Strip title rows, notes, and non-data cells.
        4. Preserve raw indicator names and treat worksheet titles as metadata rather than numeric observations.
        5. Validate numeric values before using them in rankings, charts, or policy insights.
        6. Surface only evidence-backed outputs in the dashboard.
        """
    )

    st.subheader("Indicator definitions and limitations")
    st.markdown(
        """
        - The dashboard works with poverty and vulnerability indicators extracted from the official workbook.
        - Poverty is not equivalent to financial exclusion. The platform clearly distinguishes poverty-based vulnerability signals from direct measures of access to banks, mobile money, or credit.
        - If financial access data are absent, findings are presented as prioritization proxies for deeper investigation rather than measured exclusion rates.
        - Some source tables may differ by geography, year, or unit. The app checks for missing values and dirty rows before presenting them.
        """
    )

    st.subheader("Download options")
    st.markdown("- Export dashboard tables as CSV reports from the Poverty Explorer and Community Comparison pages.")
    st.markdown("- Use the official NISR workbook or an uploaded workbook as the data source of record.")

    st.subheader("Project documentation")
    st.markdown("IMIBEREHO is designed to support policymakers, researchers, NGOs, and financial institutions in identifying where poverty vulnerability is concentrated and where follow-up financial inclusion interventions may be justified.")
