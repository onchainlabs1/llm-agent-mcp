# Audit Narrative (Portfolio Demo)

Purpose: concise overview of the demo AIMS, evidence cadence, and how to review artifacts.

Scope and boundaries
- In-scope: agent core, MCP integration, CRM/ERP/HR services, dashboard, documentation set (Clauses 4–10).
- Out of scope: external LLM infrastructure and hosting platforms (simulated via API stubs when needed).

Operational cadence (simulated, clearly labeled)
- Evidence cycles produced via `scripts/simulate_cycle.py` (run weekly).
- Each cycle generates: Internal Audit report (simulated independence), Management Review minutes, one Change, one Incident (resolved), one CAPA (implemented; effectiveness verified next cycle).

Controls implemented (high level)
- Structured JSON logs with rotation (`logs/iso_audit_trail.json`).
- Prompt input sanitization/validation; bias flags; output fact-checking; integrity hashing.
- SoA and Risk Register with traceability.

How to review
- Dashboard tabs: Overview, Docs & SoA, Risks, Audit Preparation (KPIs + buttons to simulate cycle and record daily log hash).
- Evidence folder: `docs/evidence/*` for CSV logs and markdown reports.

Caveats
- This is a functional portfolio demo. All simulated artifacts are labeled “Simulated”. No production data.


