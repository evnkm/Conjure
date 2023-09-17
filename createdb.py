import pandas as pd
import pickle

from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.docstore.document import Document
# from langchain.vectorstores import Chroma

import chromadb

# path = "/path/to/image-to-description/dataframe"
path = "./demo-dataset.csv"

df = pd.read_csv(path)

documents = []
metadatas = []
ids = []

for index, row in df.iterrows(): 
    text = row["description"]
    metadata = {
        "id": row["id"], 
        "filename": row["filename"]
    }

    documents.append(text)
    metadatas.append(metadata)
    ids.append(str(row["id"]))


# load an open-source embedding model from huggingface
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./db")

collection = client.create_collection(name="demo-dataset", embedding_function=embedding_function.embed_documents)
collection.add(
    documents=documents, 
    metadatas=metadatas, 
    ids=ids
)

vectors = embedding_function.embed_documents(documents)
df["embeddings"] = vectors
print(df)
df.to_csv(path)



