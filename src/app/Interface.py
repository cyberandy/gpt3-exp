import streamlit as st
import streamlit.components.v1 as components
from time import sleep
import base64

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)