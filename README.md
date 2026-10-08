# IMIBEREHO

Rwanda Financial Inclusion & Poverty Intelligence Platform

## Overview
IMIBEREHO is a Streamlit-based decision-support dashboard for Rwanda’s poverty and financial inclusion analysis. It helps policymakers, NGOs, financial institutions, and researchers understand where poverty vulnerability is concentrated and where deeper financial inclusion follow-up may be justified.

The platform is designed for the National Institute of Statistics of Rwanda (NISR) 2026 Big Data Hackathon under the Financial Inclusion & Poverty Reduction track.

## Problem statement
Poverty and vulnerability are not evenly distributed across Rwanda. Local institutions need a transparent way to identify vulnerable communities, understand which indicators matter most, and prioritize interventions without overstating what the available data can prove.

This application focuses on real evidence from the official NISR EICV7 Rwanda Poverty Profile workbook and makes the distinction explicit:

- Poverty vulnerability is a useful targeting proxy.
- Financial exclusion is a separate concept that requires direct financial-access data.
- The dashboard presents poverty-based prioritization signals clearly, not measured exclusion rates.

## Hackathon track
National Institute of Statistics of Rwanda (NISR) Big Data Hackathon 2026
Track: Financial Inclusion & Poverty Reduction

## Application features
- Executive dashboard with validated national indicators
- Poverty explorer with filters for geography and indicator type
- Financial inclusion intelligence view with poverty-based prioritization proxies
- Intervention priority engine with adjustable weights and explainable scoring
- Community comparison module for side-by-side analysis
- Data and methodology documentation
- Downloadable CSV exports for analysis
- Robust handling of workbook downloads, invalid data, and missing values

## Technology stack
- Python
- Streamlit
- Pandas
- Plotly
- OpenPyXL
- Requests
- Pytest

## Dataset sources
Official source:
https://statistics.gov.rw/sites/default/files/documents/2025-05/EICV7_Tables_Rwanda_Poverty_Profile.xlsx

The application automatically attempts to download the official workbook, and it supports manual Excel upload as a fallback if the source is unavailable.

## Installation
```bash
git clone https://github.com/kudakwashechikovo17/rwanda-inclusion-lab.git
cd rwanda-inclusion-lab
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Usage
1. Open the local Streamlit app.
2. Load the official NISR dataset or upload an Excel workbook from the sidebar.
3. Explore the dashboard, poverty explorer, and intervention engine.
4. Export filtered tables for review or sharing.
5. Review methodology notes before using the prioritization outputs for policy design.

## Methodology
The platform reads each worksheet in the EICV7 workbook, identifies likely header rows, removes titles and notes, and retains only rows that contain valid numeric observations. The data-cleaning layer strips obvious metadata rows and avoids treating workbook titles as statistical evidence.

Priority scoring is then performed using explainable, user-adjustable weights. The results are recommendations for follow-up investigation, not direct financial exclusion rates.

## Limitations
- The dashboard relies on the official poverty workbook as the evidence base.
- Poverty data do not directly measure formal financial inclusion.
- Financial exclusion requires separate access data, such as bank account, mobile money, or credit indicators.
- Source worksheets may vary in structure, merged cells, or row layout.
- The platform presents only validated numeric outputs and clearly labels proxy-based findings.

## Screenshots
Screenshots can be added here after the app is deployed or during presentation review.

## GitHub repository
Repository: https://github.com/kudakwashechikovo17/rwanda-inclusion-lab

## Future improvements
- Add direct financial access data from FinScope or similar datasets
- Integrate district-level geospatial visualization
- Add a richer intervention recommendation engine tied to local policy programs
- Include more explicit year-over-year poverty trend views
- Expand data validation and indicator taxonomy for other Rwanda household surveys

## Contribution to poverty reduction and financial inclusion
IMIBEREHO helps decision-makers identify where vulnerability is concentrated and where financial inclusion programs may need additional evidence, outreach, and product design. It supports smarter allocation of resources while keeping the distinction between poverty vulnerability and direct financial exclusion transparent.
