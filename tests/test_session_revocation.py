from datetime import timedelta
from simap.models import IndustrialContext, Outcome
from simap.session_manager import SessionManager

def test_session_creation_and_audit(ctx,policy):
 m=SessionManager(policy)
 decision,s=m.request(ctx)
 assert decision.outcome==Outcome.ALLOW and s.state=="ACTIVE"
 assert m.audit.events[0].session_id==s.session_id
 assert m.audit.events[0].outcome=="ALLOW"

def test_denial_creates_no_session(data,policy):
 m=SessionManager(policy)
 decision,s=m.request(IndustrialContext.model_validate({**data,"device_approved":False}))
 assert decision.outcome==Outcome.DENY and s is None and not m.sessions
 assert m.audit.events[0].outcome=="DENY"

def test_expired_permit_revokes(data,ctx,policy):
 m=SessionManager(policy); _,s=m.request(ctx)
 data.update(permit_status="expired",requested_at="2026-10-15T10:01:00+00:00")
 result=m.recheck(s.session_id,IndustrialContext.model_validate(data))
 assert result.state=="REVOKED" and "PERMIT_NOT_VALID" in result.end_reason
 assert m.audit.events[-1].event_type=="SESSION_END"

def test_context_swap_revokes(data,ctx,policy):
 m=SessionManager(policy); _,s=m.request(ctx)
 data.update(user_id="other-user",requested_at="2026-10-15T10:01:00+00:00")
 assert m.recheck(s.session_id,IndustrialContext.model_validate(data)).end_reason=="CONTEXT_MISMATCH"

def test_expiry_and_no_resurrection(data,ctx,policy):
 m=SessionManager(policy); _,s=m.request(ctx)
 data["requested_at"]="2026-10-15T10:21:00+00:00"
 result=m.recheck(s.session_id,IndustrialContext.model_validate(data))
 assert result.state=="EXPIRED"
 assert m.recheck(s.session_id,ctx).state=="EXPIRED"

def test_admin_revoke_is_idempotent(ctx,policy):
 m=SessionManager(policy); _,s=m.request(ctx)
 m.revoke(s.session_id,at=ctx.requested_at,reason="ADMIN_REVOKED")
 m.revoke(s.session_id,at=ctx.requested_at)
 assert s.state=="REVOKED"
 assert len([x for x in m.audit.events if x.event_type=="SESSION_END"])==1

def test_tightening_permit_window_never_extends_session(data,ctx,policy):
 m=SessionManager(policy); _,s=m.request(ctx)
 old=s.expires_at
 data.update(permit_end="2026-10-15T10:05:00+00:00",requested_at="2026-10-15T10:01:00+00:00")
 assert m.recheck(s.session_id,IndustrialContext.model_validate(data)).expires_at < old
