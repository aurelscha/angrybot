# How to run

git clone

in backend add a *models* directory, and put *Llama-3.2-3B-Instruct-Q8_0.gguf* inside it

model : https://huggingface.co/hugging-quants/Llama-3.2-3B-Instruct-Q8_0-GGUF/blob/main/llama-3.2-3b-instruct-q8_0.gguf

in root directory :
```
docker-compose up --build
```

wait for the model and fastapi server to start (can take 2 min)
you should see : 

```
backend-1   | INFO:     Started server process [1]
backend-1   | INFO:     Waiting for application startup.
backend-1   | INFO:     Application startup complete.
backend-1   | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

and hf : http://localhost/
