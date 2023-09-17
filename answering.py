import modal 
import pandas as pd

path = "./demo-dataset_600.csv"
llama = modal.Function.lookup("tgi-Llama-2-70b-chat-hf", "Model.generate")
df = pd.read_csv(path)

def qna(imagename, question): 
    subset = df.loc[df["filename"] == "./images/" + imagename]
    # print(subset)
    desc = subset["description"].values[0]
    prompt = f"You'll be given a question and relevant context. Provide a short answer \
        to the question using only the information provided to you in the context. Do not \
        use any other sources to formulate your answer. Your answer should only contain \
        information that is not in the context. If the context does not contain enough \
        information to answer the question, say \'I don't know.\'. The question is \'{question}\'. \
        The context is \'{desc}\'."
    
    return llama.remote(prompt)

if __name__ == "__main__": 
    print(qna("photo-1433162653888-a571db5ccccf.jpg", "Where is the bird sitting?"))