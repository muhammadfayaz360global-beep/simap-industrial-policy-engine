import json
from pathlib import Path
from simap.models import Policy

def load_policy(path: str | Path) -> Policy:
    return Policy.model_validate(json.loads(Path(path).read_text()))
