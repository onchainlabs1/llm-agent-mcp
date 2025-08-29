---
owner: Compliance Officer
version: 1.1
approved_by: Dr. Sarah Chen (AI System Lead)
approved_on: 2025-01-18
next_review: 2025-07-18
---

# Data Protection Impact Assessment (DPIA) – Example 001

## 1. Overview
- System: llm-agent-mcp
- Scope: LLM agent and business services (CRM, ERP, HR)
- Assessed by: Compliance Officer
- Date: 2025-01-18

## 2. Lawful Basis
Legitimate interests for internal demonstration and portfolio purposes. No production personal data used; demo datasets only.

## 3. Data Flows
Demo JSON datasets in `data/*.json` are read by services; no external PII processing or sharing.

## 4. Risks
- Data leakage via logs
- Improper access to demo data
- Excessive retention of logs/data

## 5. Mitigations
- Access controls (repo permissions)
- Data minimization (demo data only)
- Retention policy for logs (rotation)
- Structured logging without sensitive fields

## 6. Residual Risk
Medium – acceptable with controls in place.

## 7. Decision
Proceed with controls; monitor and review every 6 months.

## 8. Evidence
- Logging config in code and dashboard Audit Trail
- Document control headers in `docs/*.md`

