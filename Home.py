import streamlit as st
from pathlib import Path
import base64
from utils import *

def main():

    # Congfiger the page attributes
    st.set_page_config(
    page_title='Ksa Vacation',
    page_icon=":Travel:",
    layout="wide")

    # Set the background and the logo
    set_background('vacation.png')
    add_logo("logo1.png")

    # Write down the title in the middle of the page
    _,col2,_= st.columns( [0.2,0.5, 0.1])
    with col2:
        st.markdown('#\n#\n#') 
        st.markdown(f'<h1 style="color:#141517;font-family: "Cooper Black";font-size:70px;">{"Want to plan your Ksa vacation?"}</h1>', unsafe_allow_html=True)

# function to render the logo image at the side bar
def add_logo(logo_url: str, height: int = 400):
    logo = f"url(data:image/png;base64,{base64.b64encode(Path(logo_url).read_bytes()).decode()})"
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                max-width: 100%;
                height: 200;
                background-image: {logo};
                background-repeat: no-repeat;
                padding-top: {height - 20}px;
                background-position: -60px 40px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
