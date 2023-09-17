import pandas as pd
import streamlit as st

path = "./demo-dataset_600.csv"
df = pd.read_csv(path)

cluster_map = {}

for ix, row in df.iterrows(): 
    cluster_id = row["cluster_label"]
    if cluster_id in cluster_map: 
        cluster_map[cluster_id].append(row["filename"])
    else: 
        cluster_map[cluster_id] = [row["filename"]]

# def get_clusters(c_id):
#     return cluster_map[c_id]

num_clusters = len(cluster_map)

st.set_page_config(layout="wide")

st.title("conjure clustering")

st.text("Select a cluster to view:")
c_id = st.slider("", 0, num_clusters-1)

images = cluster_map[c_id]
n = len(images) // 3

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(images[:n])
    with col2:
        st.image(images[n:2*n])
    with col3:
        st.image(images[2*n:])

