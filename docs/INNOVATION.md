# Candidate technical contribution and differentiation

SIMAP investigates **industrial policy-to-session orchestration**: binding
identity, role, site/zone, shift, permit, task and approved endpoint conditions
to the creation and continuous validity of a task-limited session. This
repository is an initial executable proof of concept for the decision model.

IAM, ABAC, MFA, Zero Trust, temporary access, session auditing and remote access
are established technologies. This project does not claim their invention, a
patent grant, independently verified novelty, or a production-ready industrial
solution. The proposed differentiation is a reliable *industrial workflow*
composition and enforcement chain, including operational-state revocation.

## Research hypotheses
1. A versioned decision function can consistently enforce permit, role, zone,
   shift and endpoint requirements for a predefined PTW task.
2. Allowed sessions can be bounded by permit and shift deadlines, and can be
   invalidated when source context changes.
3. Auditable decisions can explicitly record the policies and reason codes used.
4. In a later implementation, adapters can acquire signed/fresh attributes from
   authoritative systems, and a real gateway can enforce sessions.
5. An eventual second site can reuse the same policy/session core with different
   configuration instead of wholly bespoke software.

## Demonstration versus future engineering
**Implemented:** data validation, allow/deny rules, bounded session records,
recheck/revoke state transitions, example JSON inputs, in-memory event records,
API wrapper and automated tests.

**Not implemented:** real identity federation, production PTW integration,
true gateway enforcement, token/session revocation, zero-local-data guarantees,
cryptographic audit integrity, multi-site tenancy, certified industrial devices,
controlled emergency override or AI risk analytics.

A named-product comparison and implementation benchmarks are required before
claiming superiority over any competing cybersecurity platform.
