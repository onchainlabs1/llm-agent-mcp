# NCR-2025-001 — Prompt Injection Handling Gap

- Date Opened: 2025-08-06
- Reporter: AIMS Manager
- Owner: Security Officer
- Clauses: 8.2 (Operation), 9.1 (Monitoring)
- Severity: Medium

## 1. Description
During review, detected that medium-risk prompt injection attempts were logged, but no user notification or rate-limiting action was triggered in some cases.

Evidence:
- app.py (SecurityMonitor.detect_prompt_injection)
- logs/actions.log (events 2025-08-05)
- iso_dashboard metrics

## 2. Containment
- Added temporary warning in UI for medium-level detections.

## 3. Root Cause
- Missing policy for non-critical injection attempts; no standardized action for medium severity.

## 4. Corrective Actions
| Action | Owner | Due Date | Evidence/Link | Status |
|---|---|---|---|---|
| Add rate-limiting for medium severity detections | Security Officer | 2025-08-15 | PR #TBD | Open |
| Add user notification banner for medium incidents | AI System Operator | 2025-08-15 | Commit #TBD | Open |

## 5. Preventive Actions
| Action | Owner | Due Date | Evidence/Link | Status |
|---|---|---|---|---|
| Add weekly review of security stats | AIMS Manager | 2025-08-20 | iso_dashboard.py | Open |

## 6. Verification of Effectiveness
- To be verified after deployment and two-week monitoring window.

## 7. Closure
- Date Closed: —
- Approver: —
