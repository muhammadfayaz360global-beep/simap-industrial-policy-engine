from datetime import datetime
from uuid import uuid4
from simap.models import Decision, IndustrialContext, Outcome, Session, Policy
from simap.policy_engine import evaluate
from simap.audit_service import InMemoryAuditLog

class SessionManager:
    """Demonstrates session decisions, NOT actual app isolation or credential revocation."""
    def __init__(self, policy: Policy, audit: InMemoryAuditLog | None = None):
        self.policy = policy
        self.audit = audit if audit is not None else InMemoryAuditLog()
        self.sessions: dict[str, Session] = {}

    def request(self, context: IndustrialContext) -> tuple[Decision, Session | None]:
        decision = evaluate(context, self.policy)
        session = None
        if decision.outcome == Outcome.ALLOW:
            session = Session(session_id=str(uuid4()), user_id=context.user_id,
                policy_id=self.policy.policy_id, policy_version=self.policy.version,
                permit_id=context.permit_id, task=context.task, site=context.site,
                zone=context.zone, device_id=context.device_id,
                created_at=context.requested_at, expires_at=decision.session_expires_at)
            self.sessions[session.session_id] = session
        self.audit.record(occurred_at=context.requested_at, event_type="ACCESS_DECISION",
            outcome=decision.outcome.value, request_id=context.request_id,
            session_id=session.session_id if session else None,
            policy_id=self.policy.policy_id, policy_version=self.policy.version,
            reason_codes=decision.reason_codes)
        return decision, session

    def recheck(self, session_id: str, context: IndustrialContext) -> Session:
        session = self.sessions[session_id]
        if session.state != "ACTIVE": return session
        now = context.requested_at
        if now >= session.expires_at:
            return self._end(session, now, "EXPIRED", "SESSION_DEADLINE")
        decision = evaluate(context, self.policy)
        immutable_matches = (context.user_id == session.user_id and
          context.permit_id == session.permit_id and context.task == session.task and
          context.site == session.site and context.zone == session.zone and
          context.device_id == session.device_id)
        if decision.outcome != Outcome.ALLOW or not immutable_matches:
            reason = "CONTEXT_MISMATCH" if not immutable_matches else ",".join(decision.reason_codes)
            return self._end(session, now, "REVOKED", reason)
        # Operational constraints can become stricter; never extend the original expiry.
        session.expires_at = min(session.expires_at, decision.session_expires_at)
        return session

    def revoke(self, session_id: str, *, at: datetime, reason: str = "ADMIN_REVOKED") -> Session:
        session = self.sessions[session_id]
        if session.state == "ACTIVE": self._end(session, at, "REVOKED", reason)
        return session

    def _end(self, session: Session, at: datetime, state: str, reason: str) -> Session:
        session.state = state
        session.ended_at = at
        session.end_reason = reason
        self.audit.record(occurred_at=at, event_type="SESSION_END", outcome=state,
            session_id=session.session_id, policy_id=session.policy_id,
            policy_version=session.policy_version, reason_codes=[reason])
        return session
