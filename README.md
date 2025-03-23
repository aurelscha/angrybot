# How to run

git clone

in backend add a models directory, and put Llama-3.2-3B-Instruct-Q8_0.gguf inside it
model : https://huggingface.co/hugging-quants/Llama-3.2-3B-Instruct-Q8_0-GGUF/blob/main/llama-3.2-3b-instruct-q8_0.gguf

in root directory :
```
docker-compose up --build
```

wait for the model and fastapi server to start (can take 2 min)

and hf : http://localhost/
