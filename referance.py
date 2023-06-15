import streamlit as st
import numpy as np
import pandas as pd
from  PIL import Image
from pathlib import Path
import base64
# from streamlit_elements import elements, mui, html
# image = Image.open(r'logo.png') #Brand logo image (optional)

def main():
    st.set_page_config(
    page_title='Smart Coach by Fixed Solutions',
    page_icon=":tennisball:",
    layout="wide")
    add_logo("logo.ico")
     
    st.write("# Welcome to Smart Coach")

    set_background('bg2.png')
   
    
    
    
# #Create two columns with different width
# col1, col2 = st.columns( [0.8, 0.2])
# with col1:               # To display the header text using css style
#     st.markdown(""" <style> .font {
#     font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
#     </style> """, unsafe_allow_html=True)
#     st.markdown('<p class="font">Upload your Document here...</p>', unsafe_allow_html=True)
    
# with col2:               # To display brand logo
#     st.image(image,  width=150)
def add_logo(logo_url: str, height: int = 300):
    """Add a logo (from logo_url) on the top of the navigation page of a multipage app.
    Taken from https://discuss.streamlit.io/t/put-logo-and-title-above-on-top-of-page-navigation-in-sidebar-of-multipage-app/28213/6

    The url can either be a url to the image, or a local path to the image.

    Args:
        logo_url (str): URL/local path of the logo
    """


    logo = f"url(data:image/png;base64,{base64.b64encode(Path(logo_url).read_bytes()).decode()})"

    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                max-width: 100%;
                height: auto;
                background-image: {logo};
                background-repeat: no-repeat;
                padding-top: {height - 40}px;
                background-position: 20px 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)



if __name__ == "__main__":
    main()
