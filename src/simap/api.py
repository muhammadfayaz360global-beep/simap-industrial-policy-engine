from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from simap.config import load_policy
from simap.models import IndustrialContext, Decision, Session
from simap.session_manager import SessionManager

# Stateless authentication is intentionally absent. Bind to loopback only for sandbox demos.
DEFAULT_POLICY = Path(__file__).resolve().parents[2] / "policies" / "ptw_access_policy.json"
manager = SessionManager(load_policy(DEFAULT_POLICY))
app = FastAPI(title="SIMAP Policy-to-Session Sandbox API", version="0.1.0",
    description="Synthetic demonstration only; NO authentication, durable audit, or actual gateway enforcement.")

class AccessResponse(BaseModel):
    decision: Decision
    session: Session | None

@app.get("/health")
def health(): return {"status": "demo-ok", "production_ready": False}

@app.post("/v1/access/evaluate", response_model=AccessResponse)
def access(context: IndustrialContext):
    decision, session = manager.request(context)
    return AccessResponse(decision=decision, session=session)

@app.post("/v1/sessions/{session_id}/recheck", response_model=Session)
def recheck(session_id: str, context: IndustrialContext):
    try: return manager.recheck(session_id, context)
    except KeyError: raise HTTPException(status_code=404, detail="Unknown session")

@app.get("/v1/sessions/{session_id}", response_model=Session)
def get_session(session_id: str):
    try: return manager.sessions[session_id]
    except KeyError: raise HTTPException(status_code=404, detail="Unknown session")

@app.get("/v1/audit")
def audit(): return manager.audit.events
