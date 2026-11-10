from datetime import datetime
from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field, model_validator

class Outcome(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REVOKE = "REVOKE"

class IndustrialContext(BaseModel):
    request_id: str = Field(min_length=1, max_length=128)
    user_id: str = Field(min_length=1, max_length=128)
    authenticated: bool
    role: str
    contractor_active: bool
    site: str
    zone: str
    shift_start: datetime
    shift_end: datetime
    permit_id: str
    permit_status: Literal["valid", "expired", "suspended", "revoked"]
    permit_start: datetime
    permit_end: datetime
    device_id: str
    device_approved: bool
    task: str
    requested_at: datetime

    @model_validator(mode="after")
    def require_aware_dates(self):
        for key in ("shift_start", "shift_end", "permit_start", "permit_end", "requested_at"):
            value = getattr(self, key)
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError(f"{key} must contain a timezone offset")
        return self

class Policy(BaseModel):
    policy_id: str
    version: str
    sites: list[str]
    zones: list[str]
    roles: list[str]
    tasks: list[str]
    max_session_minutes: int = Field(gt=0, le=120)
    require_active_contractor: bool = True

class Decision(BaseModel):
    request_id: str
    outcome: Outcome
    reason_codes: list[str]
    policy_id: str
    policy_version: str
    evaluated_at: datetime
    session_expires_at: datetime | None = None
    permitted_task: str | None = None

class Session(BaseModel):
    session_id: str
    user_id: str
    policy_id: str
    policy_version: str
    permit_id: str
    task: str
    site: str
    zone: str
    device_id: str
    created_at: datetime
    expires_at: datetime
    state: Literal["ACTIVE", "REVOKED", "EXPIRED"] = "ACTIVE"
    ended_at: datetime | None = None
    end_reason: str | None = None

class AuditEvent(BaseModel):
    event_id: str
    occurred_at: datetime
    event_type: str
    request_id: str | None = None
    session_id: str | None = None
    policy_id: str | None = None
    policy_version: str | None = None
    outcome: str
    reason_codes: list[str] = Field(default_factory=list)
