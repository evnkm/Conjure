from flask import Flask, request
import json

from querydb import query
from answering import qna 


def llava(imagename, prompt): 
    return "Not implemented yet, but it's cute you thought it was."

app = Flask(__name__)

@app.route('/')
def hello_world(): 
    return "Welcome to Conjure API"

@app.route('/filter', methods=["POST"])
def filter_images():
    data = json.loads(request.data)
    q = data['query']
    return json.dumps({'images': [name[9:] for name in query(q, 10)]}) # List of filenames of images.

@app.route('/qna', methods=["POST"])
def rest_qna(): 
    data = json.loads(request.data)
    print(data)
    imagename, prompt = data["filename"], data["prompt"]
    return json.dumps({'response': qna(imagename, prompt)}) # String - the response to prompt from the VLM

if __name__ == "__main__": 
    app.run()