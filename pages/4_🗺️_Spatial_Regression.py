import streamlit as st
from streamlit.components.v1 import html


# Page config
st.set_page_config(
    page_title="Spatial Regression",
    page_icon="inputs/airbnb.png",
    initial_sidebar_state="expanded",
    layout="wide"
)

with open('inputs/spatial_regression.html', 'r', encoding='utf-8') as f:
    html_file = f.read()

# Display HTML file
html(html_file, height=3500)

