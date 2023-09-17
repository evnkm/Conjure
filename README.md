# conjure

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

4. Navigate to `localhost:3000` to view the application.