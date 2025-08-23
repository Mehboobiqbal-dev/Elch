#!/usr/bin/env python3
import uvicorn
from main import application

if __name__ == "__main__":
    print("Starting server directly...")
    uvicorn.run(application, host="0.0.0.0", port=8000, log_level="info")