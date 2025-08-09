## Evidence Index – llm-agent-mcp (ISO/IEC 42001:2023)

Purpose: single entry-point mapping each requirement/control to concrete evidence in this repository (documents, code, logs, tests). All links are relative to the repo root.

### 1) Governance, Policy, Roles (Clauses 4–5; Annex A.2–A.3)

| Topic | Evidence | Owner | Last Reviewed |
|---|---|---|---|
| Scope and Boundaries | docs/Clause4_Context_new/AIMS_Scope_and_Boundaries.md | AIMS Manager | 2025-08-06 |
| Context & Stakeholders | docs/Clause4_Context_new/AIMS_Context_and_Stakeholders.md | AIMS Manager | 2025-08-06 |
| AI Policy | docs/Clause5_Leadership_new/AI_Management_Policy.md | Product Owner | 2025-08-06 |
| Acceptable Use | docs/Clause5_Leadership_new/AI_Acceptable_Use_Policy.md | Security Lead | 2025-08-06 |
| Roles & Responsibilities (RACI) | docs/Clause5_Leadership_new/AIMS_Roles_and_Responsibilities.md | AIMS Manager | 2025-08-06 |
| Concern Reporting | docs/Clause5_Leadership_new/AI_Concern_Reporting_Procedure.md | Compliance Lead | 2025-08-06 |

### 2) Planning – Risk, Objectives, SoA (Clause 6)

| Topic | Evidence | Owner | Last Reviewed |
|---|---|---|---|
| Risk Procedure | docs/Clause6_Planning_new/AI_Risk_Management_Procedure.md | Risk Owner | 2025-08-06 |
| Risk Register | docs/Clause6_Planning_new/AI_Risk_Register.csv | Risk Owner | 2025-08-06 |
| Objectives & KPIs | docs/Clause6_Planning_new/AI_Objectives_and_Planning.md | AIMS Manager | 2025-08-06 |
| Statement of Applicability | docs/Clause6_Planning_new/Statement_of_Applicability.csv | Compliance Lead | 2025-08-06 |
| Change Management | docs/Clause6_Planning_new/AI_Change_Management_Procedure.md | Engineering Lead | 2025-08-06 |

### 3) Support (Clause 7)

| Topic | Evidence |
|---|---|
| Resources | docs/Clause7_Support/AIMS_Resources.md |
| Competence & Training | docs/Clause7_Support/AIMS_Competence_and_Training.md |
| Awareness & Communication | docs/Clause7_Support/AIMS_Awareness_and_Communication.md |
| Document Control | docs/Clause7_Support/AIMS_Document_Control_Procedure.md |

### 4) Operation (Clause 8)

| Topic | Evidence | Code Links |
|---|---|---|
| Operational Planning & Control | docs/Clause8_Operation/AI_Operational_Planning_and_Control.md | agent/agent_core.py, agent/tools_mcp_client.py |
| Impact Assessment | docs/Clause8_Operation/AI_System_Impact_Assessment.md | mcp_server/*.json |
| Data Management | docs/Clause8_Operation/AI_Data_Management_Procedure.md | services/*, logs/actions.log |
| Third-party Requirements | docs/Clause8_Operation/AI_Third_Party_and_Customer_Requirements.md | config, env vars |
| Incident Response | docs/Clause8_Operation/AI_Incident_Response_Procedure.md | GitHub Issues / PRs |

### 5) Performance Evaluation (Clause 9)

| Topic | Evidence |
|---|---|
| Performance Monitoring & Measurement | docs/Clause9_Performance_Evaluation/AI_Performance_Monitoring_and_Measurement.md |
| Internal Audit Procedure | docs/Clause9_Performance_Evaluation/AI_Internal_Audit_Procedure.md |
| Management Review | docs/Clause9_Performance_Evaluation/AI_Management_Review.md |
| Continuous Improvement Loop | docs/Clause9_Performance_Evaluation/AI_Continuous_Improvement.md |

### 6) Improvement (Clause 10)

| Topic | Evidence | Templates |
|---|---|---|
| Nonconformity & Corrective Action | docs/Clause10_Improvement/AI_Nonconformity_and_Corrective_Action.md | docs/templates/NCR_CAPA_Template.md |
| Continual Improvement | docs/Clause10_Improvement/AI_Continual_Improvement.md |  |

### 7) Additional Evidence

| Topic | Evidence |
|---|---|
| Hours Log (eligibility 300h) | project_hours_log.md, project_hours_log.csv |
| ISO Dashboard | iso_dashboard.py |
| ISO Docs Browser | iso_docs.py |
| Screenshots | docs/screenshots/SCREENSHOTS.md |

Notes:
- All document owners are responsible for quarterly review (default). Update the “Last Reviewed” column after each revision.
- For any control marked Partial/No in the SoA, the CAPA template must be opened and tracked until closure.


