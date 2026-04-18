import streamlit as st

def render_footer(sidebar=False):
    text = "© 2026 Made with "
    if sidebar:
        st.sidebar.markdown("---")
        st.sidebar.markdown("© 2026 Made by [Bharath.K](https://www.linkedin.com/in/4bharathk/)")
    else:
        st.markdown(f"<div class='custom-footer'>{text}</div>", unsafe_allow_html=True)
