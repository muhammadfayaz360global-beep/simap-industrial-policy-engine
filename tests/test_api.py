from fastapi.testclient import TestClient
from simap.api import app, manager

def test_api_health():
 r=TestClient(app).get("/health")
 assert r.status_code==200 and not r.json()["production_ready"]

def test_api_access_and_get(data):
 c=TestClient(app)
 r=c.post("/v1/access/evaluate",json=data)
 assert r.status_code==200
 payload=r.json()
 assert payload["decision"]["outcome"]=="ALLOW"
 session_id=payload["session"]["session_id"]
 assert c.get(f"/v1/sessions/{session_id}").json()["state"]=="ACTIVE"

def test_api_validation_rejects_naive_time(data):
 data["requested_at"]="2026-10-15T10:00:00"
 assert TestClient(app).post("/v1/access/evaluate",json=data).status_code==422

def test_missing_session():
 assert TestClient(app).get("/v1/sessions/nonexistent").status_code==404
