import chromadb
from langchain.embeddings import HuggingFaceEmbeddings

client = chromadb.PersistentClient(path="./db")

embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

collection = client.get_collection(name="demo-dataset", embedding_function=embedding_function.embed_documents)

def query(prompt, n=5): 
    vectors = embedding_function.embed_documents([prompt])
    return collection.query(
        query_embeddings=vectors,
        n_results=n
    )


