# 🇷🇼 Rwanda Inclusion Lab

A runnable Streamlit prototype for **NISR 2026 Hackathon — Track 2: Financial Inclusion & Poverty Reduction**.

## Research question
Where are poverty-related vulnerabilities concentrated in Rwanda, and where should financial-inclusion initiatives investigate further?

**Important:** The EICV7 poverty-profile workbook does **not**, by itself, measure financial exclusion. The app does not invent financial-access statistics or imply causation.

## Features
- Downloads the official NISR EICV7 Excel workbook (or accepts an uploaded copy if the download is blocked)
- Browses worksheets and searches for poverty-related rows
- Charts selected numeric columns and exports them to CSV
- Explains the limits of using poverty data to target financial-inclusion research

## Run locally
```bash
git clone https://github.com/YOUR_USERNAME/rwanda-inclusion-lab.git
cd rwanda-inclusion-lab
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```
Then open the local URL shown by Streamlit.

## Push to GitHub
Create an empty **public** repository named `rwanda-inclusion-lab`, then run:
```bash
git init
git add .
git commit -m "Initial Rwanda Inclusion Lab prototype"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/rwanda-inclusion-lab.git
git push -u origin main
```
Replace `YOUR_USERNAME` with your actual GitHub username. This archive is not automatically connected to your account.

## Deploy
1. Push the repository to GitHub.
2. Open https://share.streamlit.io and choose **Create app**.
3. Select the repository, branch `main`, and entrypoint `app.py`.
4. Deploy and share the public app URL. If NISR blocks server downloads, upload the workbook through the app sidebar.

## Dataset
National Institute of Statistics of Rwanda (NISR), EICV7 Rwanda Poverty Profile tables:
https://statistics.gov.rw/sites/default/files/documents/2025-05/EICV7_Tables_Rwanda_Poverty_Profile.xlsx

## Next improvement
Add a separately sourced financial-access dataset with matching area definitions and periods; report financial exclusion directly, and compare it with poverty carefully.

## Hackathon disclosure
Disclose AI assistance and acknowledge NISR data in your submission. Review the competition's originality and eligibility requirements.
