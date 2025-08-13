#!/usr/bin/env python3
"""
Simulate one operational cycle for the ISO/IEC 42001 portfolio demo.

Adds one row to core evidence CSVs and creates brief markdown artifacts for
an internal audit report and a management review minutes file.

All entries are clearly labeled as Simulated and dated with current date.
"""
import csv
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVID = ROOT / "docs" / "evidence"


def today() -> str:
    return datetime.date.today().isoformat()


def append_row(csv_path: Path, headers: list[str], row: list[str]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    exists = csv_path.exists()
    with csv_path.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(headers)
        w.writerow(row)


def simulate_internal_audit() -> None:
    audit_id = f"AUD-{datetime.date.today().year}-{datetime.date.today().strftime('%m%d')}"
    report_path = EVID / f"Internal_Audit_Report_{audit_id}.md"
    report_path.write_text(
        f"""# Internal Audit Report {audit_id} (Simulated)\n\nDate: {today()}\nAuditor: Independent Reviewer (Simulated)\nIndependence: Attested\nScope: Clauses 6–9 (sampling)\n\nFindings:\n- Minor documentation completeness gaps in SoA (Owner/Evidence missing for 2 controls).\n- Recommendation: close gaps within 7 days.\n\nConclusions:\n- Overall effective with minor improvements required.\n\n""",
        encoding="utf-8",
    )
    append_row(
        EVID / "internal_audit_log.csv",
        [
            "AuditID",
            "Date",
            "Auditor",
            "Scope",
            "Findings",
            "NCRsRaised",
            "CAPAsRaised",
            "Status",
            "ReportLink",
        ],
        [
            audit_id,
            today(),
            "Independent Reviewer (Simulated)",
            "Clauses 6-9",
            "Minor SoA completeness gaps",
            "1",
            "1",
            "Closed",
            f"docs/evidence/{report_path.name}",
        ],
    )


def simulate_management_review() -> None:
    mr_id = f"MR-{datetime.date.today().year}-{datetime.date.today().strftime('%m%d')}"
    mr_path = EVID / f"Management_Review_Minutes_{mr_id}.md"
    mr_path.write_text(
        f"""# Management Review Minutes {mr_id} (Simulated)\n\nDate: {today()}\nAttendees: CEO, CTO, Compliance (Simulated)\n\nDecisions:\n- Approve CAPA to close SoA evidence gaps. Owner: Compliance, Due: +7d.\n- Schedule next internal audit in 2 weeks with independent reviewer.\n\nActions:\n- Update Risk Register treatment progress for R001, R002.\n- Add second supplier due diligence artifact next cycle.\n\n""",
        encoding="utf-8",
    )


def simulate_change_incident_capa() -> None:
    change_id = f"CHG-{datetime.date.today().year}-{datetime.date.today().strftime('%m%d')}"
    append_row(
        EVID / "change_log.csv",
        [
            "ChangeID",
            "Date",
            "Requester",
            "Description",
            "Impact",
            "ApprovalStatus",
            "ApprovedBy",
            "LinkedPR",
            "RollbackPlan",
            "EvidenceLink",
        ],
        [
            change_id,
            today(),
            "AI Manager",
            "SoA completeness remediation (add Owner/Evidence)",
            "Low",
            "Approved",
            "CTO",
            "https://github.com/onchainlabs1/llm-agent-mcp",
            "Revert SoA edits if needed",
            "docs/Clause6_Planning_new/Statement_of_Applicability.csv",
        ],
    )

    incident_id = f"INC-{datetime.date.today().year}-{datetime.date.today().strftime('%m%d')}"
    append_row(
        EVID / "incident_log.csv",
        [
            "IncidentID",
            "Date",
            "Severity",
            "ReportedBy",
            "Description",
            "Status",
            "RootCause",
            "Containment",
            "CorrectiveAction",
            "PreventiveAction",
            "ResolutionDate",
            "EvidenceLink",
        ],
        [
            incident_id,
            today(),
            "Low",
            "Compliance",
            "Documentation gap detected in SoA",
            "Resolved",
            "Process oversight",
            "Review SoA fields",
            "Add missing Owner/Evidence",
            "Add pre-commit check",
            today(),
            "docs/Clause6_Planning_new/Statement_of_Applicability.csv",
        ],
    )

    capa_id = f"CAPA-{datetime.date.today().year}-{datetime.date.today().strftime('%m%d')}"
    append_row(
        EVID / "capa_log.csv",
        [
            "CAPAID",
            "Date",
            "RelatedNCR",
            "Description",
            "Owner",
            "DueDate",
            "Status",
            "EffectivenessCheckDate",
            "EvidenceLink",
        ],
        [
            capa_id,
            today(),
            "NCR-Portfolio",
            "Close SoA Owner/Evidence gaps",
            "Compliance Officer",
            (datetime.date.today() + datetime.timedelta(days=7)).isoformat(),
            "Implemented",
            (datetime.date.today() + datetime.timedelta(days=14)).isoformat(),
            "docs/Clause6_Planning_new/Statement_of_Applicability.csv",
        ],
    )


def main() -> None:
    simulate_internal_audit()
    simulate_management_review()
    simulate_change_incident_capa()
    print("Simulated cycle recorded. All entries labeled as Simulated.")


if __name__ == "__main__":
    main()


