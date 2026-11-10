from datetime import datetime
from uuid import uuid4
from simap.models import AuditEvent

class InMemoryAuditLog:
    """Demo-only log. Not immutable, durable, or suitable for compliance evidence."""
    def __init__(self): self.events: list[AuditEvent] = []
    def record(self, *, occurred_at: datetime, event_type: str, outcome: str,
               request_id: str | None = None, session_id: str | None = None,
               policy_id: str | None = None, policy_version: str | None = None,
               reason_codes: list[str] | None = None) -> AuditEvent:
        event = AuditEvent(event_id=str(uuid4()), occurred_at=occurred_at,
                           event_type=event_type, outcome=outcome, request_id=request_id,
                           session_id=session_id, policy_id=policy_id,
                           policy_version=policy_version, reason_codes=reason_codes or [])
        self.events.append(event)
        return event
