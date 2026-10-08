import streamlit as st

from utils.data_loader import get_dataset_context


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="brand-box">
                <div class="brand-mark">IMIBEREHO</div>
                <div class="brand-subtitle">Rwanda Financial Inclusion & Poverty Intelligence</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("Turning data into opportunities for every Rwandan.")

        uploaded_file = st.file_uploader("Upload EICV7 workbook (.xlsx)", type=["xlsx"], key="eicv7_upload")
        if uploaded_file is not None:
            context = get_dataset_context(uploaded_file=uploaded_file)
            st.session_state["dataset_context"] = context
            st.session_state["dataset_loaded"] = True
        else:
            if st.button("Load official NISR dataset"):
                try:
                    st.session_state["dataset_context"] = get_dataset_context()
                    st.session_state["dataset_loaded"] = True
                    st.success("Official NISR dataset loaded successfully.")
                except Exception as exc:
                    st.warning("The official dataset could not be downloaded automatically. Please upload a workbook manually.")
                    st.caption(str(exc))

        st.markdown("---")
        st.caption("Data sources")
        if "dataset_context" in st.session_state:
            context = st.session_state["dataset_context"]
            source = context["source"]
            st.caption(f"Source: {source.upper()} workbook")
            st.caption(f"Worksheets: {len(context['sheet_summaries'])}")
        else:
            st.caption("No dataset loaded")

        return uploaded_file
