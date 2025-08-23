import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Simple FastAPI app without heavy imports
app = FastAPI(
    title="Elch AI Agent",
    description="AI Agent API",
    version="1.0.0"
)

# Create alias for uvicorn compatibility
application = app

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Elch AI Agent is running", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "elch-ai-agent"}

@app.get("/docs")
def get_docs():
    return {"message": "API documentation available at /docs"}

@app.post("/chat")
def chat_endpoint(message: dict):
    return {
        "response": "This is a simplified version. Full functionality will be restored once imports are fixed.",
        "status": "success"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)