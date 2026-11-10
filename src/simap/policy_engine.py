from datetime import timedelta
from simap.models import Decision, IndustrialContext, Outcome, Policy

def evaluate(context: IndustrialContext, policy: Policy) -> Decision:
    """Deterministic deny-by-default decision; caller supplies trusted context and clock."""
    now = context.requested_at
    reasons: list[str] = []
    if not context.authenticated: reasons.append("IDENTITY_UNVERIFIED")
    if policy.require_active_contractor and not context.contractor_active: reasons.append("CONTRACTOR_INACTIVE")
    if context.role not in policy.roles: reasons.append("ROLE_NOT_PERMITTED")
    if context.site not in policy.sites: reasons.append("SITE_NOT_PERMITTED")
    if context.zone not in policy.zones: reasons.append("ZONE_NOT_PERMITTED")
    if context.task not in policy.tasks: reasons.append("TASK_NOT_PERMITTED")
    if not context.device_approved: reasons.append("DEVICE_NOT_APPROVED")
    if not context.shift_start <= now < context.shift_end: reasons.append("SHIFT_NOT_ACTIVE")
    if context.permit_status != "valid": reasons.append("PERMIT_NOT_VALID")
    if not context.permit_start <= now < context.permit_end: reasons.append("PERMIT_OUTSIDE_WINDOW")
    if context.shift_end <= context.shift_start: reasons.append("INVALID_SHIFT_WINDOW")
    if context.permit_end <= context.permit_start: reasons.append("INVALID_PERMIT_WINDOW")
    if reasons:
        return Decision(request_id=context.request_id, outcome=Outcome.DENY,
                        reason_codes=reasons, policy_id=policy.policy_id,
                        policy_version=policy.version, evaluated_at=now)
    expiry = min(now + timedelta(minutes=policy.max_session_minutes), context.shift_end, context.permit_end)
    if expiry <= now:
        return Decision(request_id=context.request_id, outcome=Outcome.DENY,
                        reason_codes=["NO_VALID_SESSION_WINDOW"], policy_id=policy.policy_id,
                        policy_version=policy.version, evaluated_at=now)
    return Decision(request_id=context.request_id, outcome=Outcome.ALLOW,
                    reason_codes=["POLICY_SATISFIED"], policy_id=policy.policy_id,
                    policy_version=policy.version, evaluated_at=now,
                    permitted_task=context.task, session_expires_at=expiry)
