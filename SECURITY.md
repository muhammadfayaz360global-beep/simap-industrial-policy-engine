# Security policy and limitations

**THIS IS NOT A PRODUCTION ACCESS-CONTROL SYSTEM.** The demonstration API has no
caller authentication, network authorisation, rate limits, persistence or secure
secrets management. The session manager stores **records**, not isolated sessions:
it cannot revoke real OAuth tokens, terminate actual VDI sessions, restrict
clipboard or enforce endpoint data cleanup. The audit store is in-memory and
modifiable, and is NOT tamper-evident compliance logging. Do not connect the API
or example policy to live PTW systems, identity services, enterprise resources,
industrial networks or real employees.

Run only on localhost with synthetic data. Do not expose port 8000 externally.
No real credentials, personal data, customer permit IDs, site maps or architecture
secrets should be committed to the repository. Avoid displaying sensitive access
contexts in unprotected logs. Report vulnerabilities privately to the project
owner using an agreed secure channel, not a public issue.

Before any production use: independent threat modelling, authenticating API
callers, strong service-to-service identity, signed/validated authoritative
attributes, trusted clock, durability and integrity-protected audit logging,
real session/gateway enforcement, revocation propagation, secure endpoint controls,
secure SDLC, penetration tests, safe OT boundaries, privacy assessment, fail-safe
review, customer HSE/IT/OT approval and implementation evidence are required.
