import streamlit as st
import numpy as np
import pandas as pd
from  PIL import Image
from pathlib import Path
import base64


def main():
    st.set_page_config(
    page_title='Ksa Vacation',
    page_icon=":Travel:",
    layout="wide")
    add_logo("logo1.png")
    col1,col2, col3= st.columns( [0.2,0.5, 0.1])
    with col2:
        st.markdown('#\n#\n#') 
        st.markdown(f'<h1 style="color:#141517;font-family: "Cooper Black";font-size:70px;">{"Want to plan your Ksa vacation?"}</h1>', unsafe_allow_html=True)

    set_background('vacation.png')
   
    
    
    

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
