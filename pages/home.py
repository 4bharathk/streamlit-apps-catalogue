import streamlit as st
from config import PAGE_CONFIG
from utils.shared import render_footer

st.sidebar.image("assets/logo.gif")

def show():
    st.title("🚀 Welcome to the Apps and Tools Catalogue!")
    st.write("Explore application demos.")


    # Load CSS
    # Custom CSS for the cards
    st.markdown("""
    <style>
        div[data-testid="stColumn"] {
            padding: 15px;
            border: 1px solid #e6e6e6;
            border-radius: 15px;
            background-color: #fcfcfc;
            transition: 0.3s;
        }
        div[data-testid="stColumn"]:hover {
            border-color: #FF4B4B;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)



    # Calculate grid layout (3 cards per row)
    cols_per_row = 3
    for i in range(1, len(PAGE_CONFIG), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(PAGE_CONFIG):           
                page_data = PAGE_CONFIG[i + j]
                if page_data['id'] != 'home':
                    with col:
                        st.subheader(f"{page_data['icon']} {page_data['title']}")
                        st.write(page_data['description'])
                        # The button that performs the navigation
                        if st.button(f"Open {page_data['title']}", key=page_data['id']):
                            st.switch_page(page_data['script_path'])

    render_footer(True)
    

if __name__ == "__main__":
    show()