# conjure

Conjure allows users to upload a dataset of images, or their entire camera roll, that we can then filter through using natural-language prompts, such as, "locate images of nature" or “pull up my pictures from pride parade 2023.” Users can also opt for a categorization of their data and automatic classification into automatic labels. Functionality to ask questions about a specific image, like, "What is the boy in this image wearing?" is also built in.

## Demo

https://youtu.be/aONAhdpodrU

## Requirements 

```
pip install chromadb langchain sentence-transformers flask modal
```

## Running

1. Host the llama LLM model using Modal. This could take a while to get up & running. 

```
modal deploy llama.py 
```

2. Run the Flask server to create the function-calling endpoints to integrate back-end with front-end. 

```
python server.py
```

3. Navigate to the `frontend/` directory and run the web application using `npm`.

```
cd frontend
npm run dev
```

4. Run the Streamlit clustering web app. 

```
streamlit run clusters.py
```

5. Open http://localhost:3000/ in your browser.

