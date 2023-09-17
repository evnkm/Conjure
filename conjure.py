import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
from PIL import Image


st.title('Conjure')


uploaded_files = st.file_uploader("Choose file(s)", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        img = Image.open(uploaded_file)

title = st.text_input(
    'Enter a prompt', 'Show me all images with a sky in the background.')
