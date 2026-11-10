import pytest
from pydantic import ValidationError
from simap.models import IndustrialContext, Policy

def test_naive_timestamp_rejected(data):
 data["requested_at"]="2026-10-15T10:00:00"
 with pytest.raises(ValidationError,match="timezone offset"):
  IndustrialContext.model_validate(data)

def test_invalid_permit_status_rejected(data):
 data["permit_status"]="unknown"
 with pytest.raises(ValidationError): IndustrialContext.model_validate(data)

def test_missing_field_rejected(data):
 del data["permit_id"]
 with pytest.raises(ValidationError): IndustrialContext.model_validate(data)

def test_policy_invalid_duration_rejected():
 with pytest.raises(ValidationError): Policy(policy_id="x",version="1",sites=[],zones=[],roles=[],tasks=[],max_session_minutes=0)
