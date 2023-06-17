import base64
import streamlit as st
from pathlib import Path

OPENAI_API_KEY = st.secrets["openAI_API"]

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

# function to render the logo image at the side bar
def add_logo(logo_url: str, height: int = 300):
    logo = f"url(data:image/png;base64,{base64.b64encode(Path(logo_url).read_bytes()).decode()})"
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                max-width: 120%;
                height: 120;
                background-image: {logo};
                background-repeat: no-repeat;
                padding-top: {height - 20}px;
                background-position: 30px 50px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
