import streamlit as st

from utils.data_loader import get_dataset_context


def render_sidebar(page_groups, active_page_title):
    with st.sidebar:
        st.markdown(
            "### :material/insights: IMIBEREHO"
        )
        st.caption("Rwanda Financial Inclusion Intelligence")

        search_query = st.text_input(
            "Search pages",
            placeholder="Search pages",
            key="sidebar_page_search",
            label_visibility="collapsed",
        ).strip().casefold()

        matching_pages = 0
        for section, grouped_pages in page_groups.items():
            visible_pages = [
                (page, icon)
                for page, icon in grouped_pages
                if not search_query or search_query in page.title.casefold()
            ]
            if not visible_pages:
                continue

            st.markdown(
                f'<div class="sidebar-section-label">{section}</div>',
                unsafe_allow_html=True,
            )
            for page, icon in visible_pages:
                if page.title == active_page_title:
                    st.markdown(
                        '<div class="sidebar-active-marker"></div>',
                        unsafe_allow_html=True,
                    )
                st.page_link(page, label=page.title, icon=icon)
                matching_pages += 1

        if matching_pages == 0:
            st.caption("No matching pages")

        st.markdown('<div class="sidebar-rule"></div>', unsafe_allow_html=True)
        st.markdown(":material/database: **DATASET**")
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

        st.markdown('<div class="sidebar-rule"></div>', unsafe_allow_html=True)
        st.markdown(":material/source: **DATA SOURCES**")
        if "dataset_context" in st.session_state:
            context = st.session_state["dataset_context"]
            source = context["source"]
            st.caption(f"Source: {source.upper()} workbook")
            st.caption(f"Worksheets: {len(context['sheet_summaries'])}")
        else:
            st.caption("No dataset loaded")

        return uploaded_file
