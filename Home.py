import streamlit as st
from utils import *

def main():

    # Congfiger the page attributes
    st.set_page_config(
    page_title='Ksa Vacation',
    page_icon=":Travel:",   
    layout="wide")

    # Set the background and the logo
    set_background('vacation.jpeg')
    add_logo("logo4.png")

    # Write down the title in the middle of the page
    _,col2,_= st.columns( [0.3,0.5, 0.1])
    with col2:
        st.title(f'Launch your joy')

    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("'<h2 style="color:#AFE1AF">Are you planning a trip to Saudi Arabia but don't know where to start? Have you ever seen a photo of a place you like and wondered where you can find something similar in Saudi Arabia?\n\n</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='font-family:font-size: 1500px' >If so, then you've come to the right place! Our website is your one-stop shop for all things Saudi Arabia tourism. We have everything you need to plan your perfect trip, from information on the best places to visit to tips on how to get around (supports English and Arabic languages).\n\n</h3>", unsafe_allow_html=True)



if __name__ == "__main__":
    main()
