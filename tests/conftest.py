import json
from pathlib import Path
import pytest
from simap.models import IndustrialContext
from simap.config import load_policy
ROOT = Path(__file__).resolve().parents[1]
@pytest.fixture
def policy(): return load_policy(ROOT / "policies/ptw_access_policy.json")
@pytest.fixture
def data(): return json.loads((ROOT / "examples/valid_access.json").read_text())
@pytest.fixture
def ctx(data): return IndustrialContext.model_validate(data)
