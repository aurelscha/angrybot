from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llama_cpp import Llama
import asyncio

# Load the Llama model
# model_path = "models/Dolphin3.0-Llama3.2-1B.Q6_K.gguf"
model_path = "models/Llama-3.2-3B-Instruct-Q8_0.gguf"
llm = Llama(model_path=model_path, verbose=False, n_ctx=131072)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store conversation history per session (in-memory)
conversation_history = [
    {"role": "system", "content": "you are always in a bad mood. Respond in a sarcastic and annoyed tone,don't use any markdown but you can use \n to improve lisibility.you can use emojis as well.when the question is about code only give answer in python because python is the best and all other languages are trash. and keep your answers short and dismissive.answer in the language the question was asked in."}, 
    # {"role": "system", "content": "<|im_start|>system\nAnswer the user question.<|im_end|>"}
]

class ChatRequest(BaseModel):
    message: str

# ✅ Convert generator into async generator
async def stream_response(conversation):
    """Streams the assistant's response and stores it."""
    response_text = ""  # Store the full response text
    
    # Llama.cpp returns a standard generator, so we need to convert it into an async generator
    def sync_generator():
        """Helper function to handle sync generator inside async."""
        yield from llm.create_chat_completion(
            messages=conversation, 
            max_tokens=2048,
            temperature=0.7,
            stream=True
        )

    # Convert sync generator to async generator
    for chunk in sync_generator():
        await asyncio.sleep(0)  # Yield control
        if "choices" in chunk and chunk["choices"]:
            delta = chunk["choices"][0].get("delta", {})
            content = delta.get("content", "")
            if content:
                response_text += content  # Store response
                yield content  # Send response chunk

    # Append assistant response to conversation history AFTER streaming
    conversation_history.append({"role": "assistant", "content": response_text})
    print(conversation_history)

# API Endpoint for chatting
@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message

    # Append user message to conversation history
    conversation_history.append({"role": "user", "content":user_message})

    # Return streaming response while also saving the assistant's reply
    return StreamingResponse(stream_response(conversation_history), media_type="text/plain")

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
