import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the DataFrame
path = "./demo-dataset_600.csv"
df = pd.read_csv(path)

# Get the document vectors

vectorizer = TfidfVectorizer(
    max_df=0.5,
    min_df=5,
    stop_words="english",
)
document_vectors = vectorizer.fit_transform(df["description"])
# print(f"n_samples: {X_tfidf.shape[0]}, n_features: {X_tfidf.shape[1]}")

# document_vectors = [list(emb) for emb in df["embeddings"]]

# for vec in document_vectors: 
#     print(len(vec))

# Define a range of cluster sizes
cluster_sizes = range(5, 20)

# Calculate the silhouette score for each cluster size
silhouette_scores = []
for cluster_size in cluster_sizes:
    kmeans = KMeans(n_clusters=cluster_size)
    cluster_labels = kmeans.fit_predict(document_vectors)
    sil_score = silhouette_score(document_vectors, cluster_labels)
    silhouette_scores.append(sil_score)

# what be the best cluster
optimal_cluster_size = cluster_sizes[silhouette_scores.index(max(silhouette_scores))]

print("Number of clusters: " + str(optimal_cluster_size))

# Perform k-means clustering with the optimal cluster size
kmeans = KMeans(n_clusters=optimal_cluster_size)
cluster_labels = kmeans.fit_predict(document_vectors)

# Add the cluster labels to the DataFrame
df["cluster_label"] = cluster_labels

# # Add a column to the DataFrame to label each image as belonging to its cluster
# df["image_cluster"] = df["cluster_label"].apply(lambda cluster_label: f"Cluster {cluster_label + 1}")

# Print the DataFrame
print(df)

df.to_csv(path)