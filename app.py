import streamlit as st
from config import PAGE_CONFIG

# 1. Setup Page List dynamically
pages = []
for p in PAGE_CONFIG:
    pages.append(st.Page(p['script_path'], title=p['title'], icon=p['icon']))

# 2. Initialize Navigation
pg = st.navigation(pages)

# 3. App Config
st.set_page_config(page_title="App Catalogue", initial_sidebar_state="collapsed",layout="wide")

def add_logo():
    st.markdown(
        """
        <style>
            /* Adjust font size of page links in the sidebar */
            [data-testid="stSidebarNav"] li p {
                font-size: 20px !important;
            }

            [data-testid="stSidebarHeader"]::before {
                content: "Apps Catalogue";
                margin-left: 10px;
                margin-top: 10px;
                font-size: 30px;
                font-family:Georgia, serif;
                color: #004aad;
                position: relative;
                top: 10px;
            }

        </style>
        """,
        unsafe_allow_html=True,
    )

with st.sidebar:
    add_logo()


# 4. Run the selected page
pg.run()