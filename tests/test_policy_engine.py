from datetime import timedelta
import pytest
from simap.models import IndustrialContext, Outcome
from simap.policy_engine import evaluate

def test_allowed_valid_context(ctx, policy):
 d=evaluate(ctx,policy)
 assert d.outcome == Outcome.ALLOW and d.permitted_task == "ptw-acknowledge"
 assert d.session_expires_at == ctx.requested_at + timedelta(minutes=20)

@pytest.mark.parametrize("change,reason", [
 ({"authenticated":False},"IDENTITY_UNVERIFIED"),
 ({"contractor_active":False},"CONTRACTOR_INACTIVE"),
 ({"role":"visitor"},"ROLE_NOT_PERMITTED"),
 ({"site":"Plant-X"},"SITE_NOT_PERMITTED"),
 ({"zone":"Zone-XX"},"ZONE_NOT_PERMITTED"),
 ({"task":"view-all-records"},"TASK_NOT_PERMITTED"),
 ({"device_approved":False},"DEVICE_NOT_APPROVED"),
 ({"permit_status":"revoked"},"PERMIT_NOT_VALID"),
 ({"requested_at":"2026-10-15T17:00:00+00:00"},"SHIFT_NOT_ACTIVE"),
 ({"requested_at":"2026-10-15T12:00:00+00:00"},"PERMIT_OUTSIDE_WINDOW"),
])
def test_deny_cases(data,policy,change,reason):
 d=evaluate(IndustrialContext.model_validate({**data,**change}),policy)
 assert d.outcome == Outcome.DENY
 assert reason in d.reason_codes
 assert d.session_expires_at is None

def test_expiry_capped_by_permit(data,policy):
 data["requested_at"]="2026-10-15T11:55:00+00:00"
 d=evaluate(IndustrialContext.model_validate(data),policy)
 assert d.outcome==Outcome.ALLOW
 assert d.session_expires_at.isoformat()=="2026-10-15T12:00:00+00:00"

def test_boundary_shift_expiry(data,policy):
 data.update(requested_at="2026-10-15T15:55:00+00:00", permit_end="2026-10-15T18:00:00+00:00")
 d=evaluate(IndustrialContext.model_validate(data),policy)
 assert d.session_expires_at.isoformat()=="2026-10-15T16:00:00+00:00"
