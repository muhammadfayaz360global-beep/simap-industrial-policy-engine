import argparse, json
from pathlib import Path
from simap.config import load_policy
from simap.models import IndustrialContext
from simap.session_manager import SessionManager

def main():
    parser = argparse.ArgumentParser(description="SIMAP offline synthetic-access demo")
    parser.add_argument("example", help="Path to context JSON")
    parser.add_argument("--policy", default=str(Path(__file__).resolve().parents[2] / "policies" / "ptw_access_policy.json"))
    args = parser.parse_args()
    engine = SessionManager(load_policy(args.policy))
    context = IndustrialContext.model_validate(json.loads(Path(args.example).read_text()))
    decision, session = engine.request(context)
    print(json.dumps({"decision": decision.model_dump(mode="json"),
                      "session": session.model_dump(mode="json") if session else None,
                      "audit": [e.model_dump(mode="json") for e in engine.audit.events]}, indent=2))
if __name__ == "__main__": main()
