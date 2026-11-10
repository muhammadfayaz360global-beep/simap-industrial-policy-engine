# Development roadmap

| Stage | Scope | Evidence gate |
|---|---|---|
| v0.1 — included | Data models, policy evaluation, constrained session records, reason codes | pytest suite passes |
| v0.2 | Authenticated, read-only connectors to synthetic PTW/shift services; attribute provenance and freshness | Contract tests, stale-source denial |
| v0.3 | Reference application gateway with real task-level enforcement; token lifecycle | Negative authorisation tests |
| v0.4 | Event-driven permit revocation, durable event stream, bounded revocation latency | Failure-injection benchmarks |
| v0.5 | Integrity-protected audit storage, safe deployment and observation | Security testing and audit review |
| v1.0 | Hardened end-to-end sandbox demonstration suitable for external technical evaluation | Independent assessment and release gate |

## 24-week linkage
Weeks 1–4: requirements and threat model; weeks 5–8: authenticated identity and
policy basis; weeks 9–12: session and workflow gateway; weeks 13–16: PTW/OTP
sandbox integration and audit; weeks 17–20: security verification; weeks 21–24:
pilot-readiness review. No live hazardous-area deployment is assumed.

All dates and milestones are planning objectives, not claims of completion.
