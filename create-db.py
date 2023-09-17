import pandas as pd
import pickle

from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.docstore.document import Document
# from langchain.vectorstores import Chroma

import chromadb

# path = "/path/to/image-to-description/dataframe"
path = "./demo-dataset/df.csv"

df = pd.read_csv(path)

# docs = []

documents = []
metadatas = []
ids = []

for index, row in df.iterrows(): 
    text = row["description"]
    metadata = {
        "id": row["id"], 
        "filename": row["filename"]
    }
    # doc = Document(page_content=text, metadata=metadata)
    # docs.append(doc)

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

# db = Chroma.from_documents(docs, embedding_function)

# db2 = Chroma(persist_directory="./", embedding_function=embedding_function)

# with open("embeddings.pkl", "wb") as f: 
#     pickle.dump(db, f)

# query = "Show me images of an office."
# docs = db.similarity_search(query, 1)

# print(docs)


