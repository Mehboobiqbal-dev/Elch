from fastapi.testclient import TestClient
import uuid
import json
import main

client = TestClient(main.app)

print("GET /")
r = client.get("/")
print(r.status_code, r.json())

email = f"check+{uuid.uuid4().hex[:8]}@example.com"
password = uuid.uuid4().hex

print("POST /signup")
r = client.post("/signup", json={"email": email, "password": password, "name": "Tester"})
print(r.status_code, r.json())

print("POST /token")
r = client.post("/token", data={"username": email, "password": password}, headers={"Content-Type": "application/x-www-form-urlencoded"})
print(r.status_code, r.json())

token = r.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

print("GET /me")
r = client.get("/me", headers=headers)
print(r.status_code, r.json())

print("GET /credentials")
r = client.get("/credentials", headers=headers)
print(r.status_code, r.json())

print("POST /chat/message")
r = client.post("/chat/message", headers=headers, json={"message": "ping"})
print(r.status_code, r.json())
