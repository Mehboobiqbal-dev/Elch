from fastapi.testclient import TestClient
import main
import json

client = TestClient(main.app)

# Create a user and token
from uuid import uuid4
email = f"llmcheck+{uuid4().hex[:8]}@example.com"
password = uuid4().hex
client.post("/signup", json={"email": email, "password": password, "name": "LLM"})
r = client.post("/token", data={"username": email, "password": password}, headers={"Content-Type": "application/x-www-form-urlencoded"})
token = r.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

print("POST /assistant/prompt (should hit intent_extractor -> Gemini)")
r = client.post("/assistant/prompt", headers=headers, json={"prompt": "List all EC2 instances on AWS"})
print(r.status_code)
try:
    print(json.dumps(r.json(), indent=2)[:800])
except Exception:
    print(r.text)

print("POST /prompt (main LLM-driven endpoint)")
r = client.post("/prompt", headers=headers, json={"prompt": "Say hello"})
print(r.status_code)
try:
    print(json.dumps(r.json(), indent=2)[:800])
except Exception:
    print(r.text)
