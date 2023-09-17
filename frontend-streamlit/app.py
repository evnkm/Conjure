import os
import streamlit as st

# from query-db import query

# DUMMY FUNCTION
def get_images(query, images):
    return images[:10]

state = st.session_state

state.prompt = ""
# state.query = ""

# if 'images' not in state:
#     state.images = ['./images/'+ name for name in os.listdir('./images')]

# def change_images(): 
#     if state.query == "": 
#         state.images = ['./images/'+ name for name in os.listdir('./images')]
#     else: 
#         state.images = get_images(state.query, state.images)

st.set_page_config(layout="wide")

st.title("conjure")

st.header("Dataset View")

st.write(state.prompt)
images = []
if state.prompt == "": 
    images = ['./images/'+ name for name in os.listdir('./images')]
else: 
    images = get_images(state.prompt, images)

n = len(images) // 3

with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image(images[:n])
    with col2:
        st.image(images[n:2*n])
    with col3:
        st.image(images[2*n:])
    with col4: 
        st.subheader("ChatBot")
        st.text_input("Enter a query: ", value=state.prompt, key="prompt")
        st.write(state.prompt)




