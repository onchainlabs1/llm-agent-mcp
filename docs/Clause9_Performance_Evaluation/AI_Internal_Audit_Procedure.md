---
owner: Compliance Officer
version: 1.0
approved_by: AIMS Manager
approved_on: 2024-12-20
next_review: 2025-06-20
---

# AI Internal Audit Procedure
*AI Management System - ISO/IEC 42001:2023 Compliance*

**Document Control:**
- **Document ID:** AIMS-IAP-001
- **Version:** 1.0
- **Date:** 2024-12-19
- **Status:** Draft
- **Owner:** AI Management Team

---

## 9.2 Internal Audit

### 9.2.1 General

The organization shall conduct internal audits at planned intervals to provide information on whether the AI management system conforms to the organization's own requirements and to the requirements of ISO/IEC 42001:2023.

#### 9.2.1.1 Internal Audit Framework

The `llm-agent-mcp` project implements a comprehensive internal audit framework that ensures regular assessment of AI management system compliance, performance, and effectiveness through systematic audit procedures and automated audit signals.

### 9.2.2 Audit Planning and Schedule

#### 9.2.2.1 Audit Frequency and Schedule

**Audit Schedule:**
- **Monthly Audits:** Automated compliance and performance audits
- **Quarterly Audits:** Comprehensive system and process audits
- **Annual Audits:** Full ISO/IEC 42001:2023 compliance audits
- **Ad-hoc Audits:** Incident-based or change-triggered audits

**Current Implementation Examples:**
```python
# Audit scheduling in services/audit_scheduler.py
from datetime import datetime, timedelta
import calendar

class AuditScheduler:
    def __init__(self):
        self.audit_schedule = {
            "monthly": {
                "frequency": "monthly",
                "day_of_month": 15,  # 15th of each month
                "audit_type": "automated_compliance",
                "scope": ["performance_metrics", "security_events", "error_logs"]
            },
            "quarterly": {
                "frequency": "quarterly",
                "months": [3, 6, 9, 12],  # March, June, September, December
                "day_of_month": 1,
                "audit_type": "comprehensive_system",
                "scope": ["full_system", "processes", "documentation", "compliance"]
            },
            "annual": {
                "frequency": "annual",
                "month": 12,  # December
                "day_of_month": 1,
                "audit_type": "iso_compliance",
                "scope": ["iso_42001_compliance", "management_review", "continuous_improvement"]
            }
        }
        self.audit_history = []
    
    def get_next_audit_date(self, audit_type: str) -> datetime:
        """Get the next scheduled audit date for a specific audit type"""
        now = datetime.now()
        
        if audit_type == "monthly":
            # Next monthly audit
            next_month = now.replace(day=1) + timedelta(days=32)
            next_month = next_month.replace(day=1)
            return next_month.replace(day=self.audit_schedule["monthly"]["day_of_month"])
        
        elif audit_type == "quarterly":
            # Next quarterly audit
            current_quarter = (now.month - 1) // 3 + 1
            next_quarter_month = current_quarter * 3
            if next_quarter_month <= now.month:
                next_quarter_month += 3
                if next_quarter_month > 12:
                    next_quarter_month = 3
                    next_year = now.year + 1
                else:
                    next_year = now.year
            else:
                next_year = now.year
            
            return datetime(next_year, next_quarter_month, 
                          self.audit_schedule["quarterly"]["day_of_month"])
        
        elif audit_type == "annual":
            # Next annual audit
            if now.month >= 12:
                next_year = now.year + 1
            else:
                next_year = now.year
            
            return datetime(next_year, 12, 1)
        
        return None
    
    def is_audit_due(self, audit_type: str) -> bool:
        """Check if an audit is due"""
        next_audit_date = self.get_next_audit_date(audit_type)
        if not next_audit_date:
            return False
        
        return datetime.now() >= next_audit_date
    
    def schedule_audit(self, audit_type: str, auditor: str, scope: list) -> dict:
        """Schedule a new audit"""
        audit = {
            "audit_id": f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "audit_type": audit_type,
            "scheduled_date": self.get_next_audit_date(audit_type).isoformat(),
            "auditor": auditor,
            "scope": scope,
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }
        
        self.audit_history.append(audit)
        return audit
```

#### 9.2.2.2 Audit Scope and Objectives

**Audit Scope Areas:**
- **System Performance:** Performance metrics and response times
- **Security Compliance:** Security controls and incident response
- **Data Management:** Data handling and privacy compliance
- **Process Compliance:** Process adherence and effectiveness
- **Documentation:** Documentation completeness and accuracy

**Current Implementation Examples:**
```python
# Audit scope definition in services/audit_scope.py
class AuditScope:
    def __init__(self):
        self.audit_areas = {
            "system_performance": {
                "description": "System performance and response metrics",
                "checklist": [
                    "LLM response time compliance",
                    "Tool execution time compliance",
                    "Error rate monitoring",
                    "Success rate tracking",
                    "Performance alert effectiveness"
                ],
                "evidence_sources": [
                    "logs/performance.log",
                    "agent/agent_core.py",
                    "api/routers/health.py"
                ]
            },
            "security_compliance": {
                "description": "Security controls and incident management",
                "checklist": [
                    "Prompt injection detection",
                    "Input validation effectiveness",
                    "Security incident response",
                    "Access control implementation",
                    "Audit logging completeness"
                ],
                "evidence_sources": [
                    "app.py",
                    "logs/security.log",
                    "agent/agent_core.py"
                ]
            },
            "data_management": {
                "description": "Data handling and privacy compliance",
                "checklist": [
                    "Data classification compliance",
                    "Schema validation effectiveness",
                    "Data retention compliance",
                    "Privacy protection measures",
                    "Data quality monitoring"
                ],
                "evidence_sources": [
                    "data/",
                    "services/",
                    "logs/actions.log"
                ]
            },
            "process_compliance": {
                "description": "Process adherence and effectiveness",
                "checklist": [
                    "MCP protocol compliance",
                    "Tool registration process",
                    "Error handling procedures",
                    "Incident response procedures",
                    "Change management process"
                ],
                "evidence_sources": [
                    "agent/tools_mcp_client.py",
                    "services/",
                    "docs/"
                ]
            },
            "documentation": {
                "description": "Documentation completeness and accuracy",
                "checklist": [
                    "ISO/IEC 42001:2023 documentation completeness",
                    "Technical documentation accuracy",
                    "Process documentation currency",
                    "Compliance documentation validity",
                    "Document control effectiveness"
                ],
                "evidence_sources": [
                    "docs/",
                    "README.md",
                    "CHANGELOG.md"
                ]
            }
        }
    
    def get_audit_checklist(self, audit_type: str) -> dict:
        """Get audit checklist for specific audit type"""
        if audit_type == "automated_compliance":
            return {
                "system_performance": self.audit_areas["system_performance"],
                "security_compliance": self.audit_areas["security_compliance"]
            }
        elif audit_type == "comprehensive_system":
            return self.audit_areas
        elif audit_type == "iso_compliance":
            return {
                "process_compliance": self.audit_areas["process_compliance"],
                "documentation": self.audit_areas["documentation"],
                "data_management": self.audit_areas["data_management"]
            }
        else:
            return {}
```

### 9.2.3 Audit Execution

#### 9.2.3.1 Automated Audit Tools

**GitHub Actions Integration:**
- **Automated Testing:** Continuous integration and testing
- **Code Quality Checks:** Automated code quality analysis
- **Security Scanning:** Automated security vulnerability scanning
- **Compliance Checks:** Automated compliance verification

**Current Implementation Examples:**
```python
# Automated audit tools in .github/workflows/audit.yml
class AutomatedAuditTools:
    def __init__(self):
        self.audit_tools = {
            "code_quality": {
                "tool": "flake8",
                "command": "flake8 agent/ services/ api/",
                "threshold": "no_errors",
                "description": "Code quality and style compliance"
            },
            "security_scanning": {
                "tool": "bandit",
                "command": "bandit -r agent/ services/ api/",
                "threshold": "low_risk_only",
                "description": "Security vulnerability scanning"
            },
            "test_coverage": {
                "tool": "pytest",
                "command": "pytest tests/ --cov=agent --cov=services --cov=api",
                "threshold": "coverage >= 80%",
                "description": "Test coverage analysis"
            },
            "dependency_check": {
                "tool": "safety",
                "command": "safety check",
                "threshold": "no_critical_vulnerabilities",
                "description": "Dependency vulnerability check"
            },
            "documentation_check": {
                "tool": "custom",
                "command": "python scripts/check_documentation.py",
                "threshold": "all_docs_present",
                "description": "Documentation completeness check"
            }
        }
    
    def run_automated_audit(self) -> dict:
        """Run all automated audit tools"""
        audit_results = {
            "timestamp": datetime.now().isoformat(),
            "tools_executed": [],
            "overall_status": "pass",
            "findings": []
        }
        
        for tool_name, tool_config in self.audit_tools.items():
            try:
                result = self.execute_audit_tool(tool_name, tool_config)
                audit_results["tools_executed"].append({
                    "tool": tool_name,
                    "status": result["status"],
                    "findings": result["findings"]
                })
                
                if result["status"] == "fail":
                    audit_results["overall_status"] = "fail"
                    audit_results["findings"].extend(result["findings"])
                
            except Exception as e:
                audit_results["tools_executed"].append({
                    "tool": tool_name,
                    "status": "error",
                    "error": str(e)
                })
                audit_results["overall_status"] = "fail"
        
        return audit_results
    
    def execute_audit_tool(self, tool_name: str, tool_config: dict) -> dict:
        """Execute a specific audit tool"""
        import subprocess
        import sys
        
        result = {
            "tool": tool_name,
            "status": "pass",
            "findings": [],
            "execution_time": 0.0
        }
        
        start_time = time.time()
        
        try:
            # Execute the tool command
            process = subprocess.run(
                tool_config["command"].split(),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            result["execution_time"] = time.time() - start_time
            
            # Analyze results based on tool type
            if tool_name == "code_quality":
                result = self.analyze_flake8_results(process, result)
            elif tool_name == "security_scanning":
                result = self.analyze_bandit_results(process, result)
            elif tool_name == "test_coverage":
                result = self.analyze_pytest_results(process, result)
            elif tool_name == "dependency_check":
                result = self.analyze_safety_results(process, result)
            elif tool_name == "documentation_check":
                result = self.analyze_documentation_results(process, result)
            
        except subprocess.TimeoutExpired:
            result["status"] = "timeout"
            result["findings"].append("Tool execution timed out")
        except Exception as e:
            result["status"] = "error"
            result["findings"].append(f"Tool execution error: {str(e)}")
        
        return result
    
    def analyze_flake8_results(self, process: subprocess.CompletedProcess, result: dict) -> dict:
        """Analyze flake8 code quality results"""
        if process.returncode != 0:
            result["status"] = "fail"
            result["findings"].append(f"Code quality issues found: {process.stdout}")
        return result
    
    def analyze_bandit_results(self, process: subprocess.CompletedProcess, result: dict) -> dict:
        """Analyze bandit security scanning results"""
        if "HIGH" in process.stdout or "CRITICAL" in process.stdout:
            result["status"] = "fail"
            result["findings"].append("High or critical security vulnerabilities found")
        return result
    
    def analyze_pytest_results(self, process: subprocess.CompletedProcess, result: dict) -> dict:
        """Analyze pytest test coverage results"""
        if process.returncode != 0:
            result["status"] = "fail"
            result["findings"].append("Test failures detected")
        
        # Check coverage percentage
        if "TOTAL" in process.stdout:
            coverage_line = [line for line in process.stdout.split('\n') if "TOTAL" in line]
            if coverage_line:
                coverage_parts = coverage_line[0].split()
                if len(coverage_parts) >= 4:
                    coverage_percent = float(coverage_parts[3].replace('%', ''))
                    if coverage_percent < 80:
                        result["status"] = "fail"
                        result["findings"].append(f"Test coverage below 80%: {coverage_percent}%")
        
        return result
```

#### 9.2.3.2 Manual Audit Procedures

**Manual Audit Steps:**
- **Documentation Review:** Review of ISO/IEC 42001:2023 documentation
- **Process Verification:** Verification of process implementation
- **System Testing:** Manual testing of system functionality
- **Interview Stakeholders:** Interviews with system users and stakeholders

**Current Implementation Examples:**
```python
# Manual audit procedures in services/manual_audit.py
class ManualAuditProcedures:
    def __init__(self):
        self.audit_procedures = {
            "documentation_review": {
                "steps": [
                    "Review Clause 4-8 documentation completeness",
                    "Verify document control procedures",
                    "Check documentation accuracy",
                    "Validate compliance with ISO/IEC 42001:2023"
                ],
                "evidence_required": [
                    "Documentation files in docs/",
                    "Document control records",
                    "Version history"
                ]
            },
            "process_verification": {
                "steps": [
                    "Verify MCP protocol implementation",
                    "Check tool registration process",
                    "Validate error handling procedures",
                    "Test incident response procedures"
                ],
                "evidence_required": [
                    "Code implementation",
                    "Log files",
                    "Configuration files"
                ]
            },
            "system_testing": {
                "steps": [
                    "Test LLM integration",
                    "Verify tool execution",
                    "Check security controls",
                    "Validate data handling"
                ],
                "evidence_required": [
                    "Test results",
                    "Performance metrics",
                    "Error logs"
                ]
            },
            "stakeholder_interviews": {
                "steps": [
                    "Interview system users",
                    "Review feedback and complaints",
                    "Assess user satisfaction",
                    "Identify improvement opportunities"
                ],
                "evidence_required": [
                    "Interview notes",
                    "Feedback records",
                    "Satisfaction surveys"
                ]
            }
        }
    
    def conduct_manual_audit(self, audit_areas: list, auditor: str) -> dict:
        """Conduct manual audit of specified areas"""
        audit_report = {
            "audit_id": f"manual_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "auditor": auditor,
            "audit_date": datetime.now().isoformat(),
            "audit_areas": audit_areas,
            "findings": [],
            "recommendations": [],
            "overall_status": "pass"
        }
        
        for area in audit_areas:
            if area in self.audit_procedures:
                area_result = self.audit_area(area, auditor)
                audit_report["findings"].extend(area_result["findings"])
                audit_report["recommendations"].extend(area_result["recommendations"])
                
                if area_result["status"] == "fail":
                    audit_report["overall_status"] = "fail"
        
        return audit_report
    
    def audit_area(self, area: str, auditor: str) -> dict:
        """Audit a specific area"""
        procedure = self.audit_procedures[area]
        
        area_result = {
            "area": area,
            "auditor": auditor,
            "audit_date": datetime.now().isoformat(),
            "steps_completed": [],
            "findings": [],
            "recommendations": [],
            "status": "pass"
        }
        
        # Execute audit steps
        for step in procedure["steps"]:
            step_result = self.execute_audit_step(step, area)
            area_result["steps_completed"].append({
                "step": step,
                "status": step_result["status"],
                "findings": step_result["findings"]
            })
            
            if step_result["status"] == "fail":
                area_result["status"] = "fail"
                area_result["findings"].extend(step_result["findings"])
                area_result["recommendations"].extend(step_result["recommendations"])
        
        return area_result
    
    def execute_audit_step(self, step: str, area: str) -> dict:
        """Execute a specific audit step"""
        step_result = {
            "step": step,
            "status": "pass",
            "findings": [],
            "recommendations": []
        }
        
        # This would contain the actual audit logic for each step
        # For now, we'll provide a framework
        
        if "documentation" in step.lower():
            step_result = self.audit_documentation_step(step)
        elif "process" in step.lower():
            step_result = self.audit_process_step(step)
        elif "testing" in step.lower():
            step_result = self.audit_testing_step(step)
        elif "interview" in step.lower():
            step_result = self.audit_interview_step(step)
        
        return step_result
    
    def audit_documentation_step(self, step: str) -> dict:
        """Audit documentation-related step"""
        result = {
            "step": step,
            "status": "pass",
            "findings": [],
            "recommendations": []
        }
        
        # Check if required documentation exists
        required_docs = [
            "docs/Clause4_Context/",
            "docs/Clause5_Leadership/",
            "docs/Clause6_Planning/",
            "docs/Clause7_Support/",
            "docs/Clause8_Operation/",
            "docs/Clause9_Performance_Evaluation/"
        ]
        
        for doc_path in required_docs:
            if not os.path.exists(doc_path):
                result["status"] = "fail"
                result["findings"].append(f"Missing documentation: {doc_path}")
                result["recommendations"].append(f"Create missing documentation: {doc_path}")
        
        return result
```

### 9.2.4 Audit Evidence and Documentation

#### 9.2.4.1 Evidence Collection

**Evidence Types:**
- **System Logs:** Performance and error logs
- **Configuration Files:** System configuration and settings
- **Code Artifacts:** Source code and implementation
- **Documentation:** ISO/IEC 42001:2023 documentation
- **Test Results:** Automated and manual test results

**Current Implementation Examples:**
```python
# Evidence collection in services/audit_evidence.py
class AuditEvidenceCollector:
    def __init__(self):
        self.evidence_sources = {
            "system_logs": [
                "logs/actions.log",
                "logs/performance.log",
                "logs/security.log",
                "logs/error.log"
            ],
            "configuration_files": [
                "config.py",
                "requirements.txt",
                "requirements-full.txt",
                ".github/workflows/ci.yml"
            ],
            "code_artifacts": [
                "agent/",
                "services/",
                "api/",
                "app.py",
                "landing.py"
            ],
            "documentation": [
                "docs/",
                "README.md",
                "CHANGELOG.md",
                "PROJECT_RULES.md"
            ],
            "test_results": [
                "tests/",
                ".coverage",
                "pytest.xml"
            ]
        }
    
    def collect_audit_evidence(self, audit_scope: list) -> dict:
        """Collect evidence for audit scope"""
        evidence = {
            "collection_date": datetime.now().isoformat(),
            "audit_scope": audit_scope,
            "evidence_files": {},
            "evidence_summary": {},
            "completeness_score": 0.0
        }
        
        total_files = 0
        collected_files = 0
        
        for scope_area in audit_scope:
            if scope_area in self.evidence_sources:
                evidence["evidence_files"][scope_area] = []
                
                for file_path in self.evidence_sources[scope_area]:
                    total_files += 1
                    
                    if os.path.exists(file_path):
                        collected_files += 1
                        file_info = self.get_file_info(file_path)
                        evidence["evidence_files"][scope_area].append(file_info)
                    else:
                        evidence["evidence_files"][scope_area].append({
                            "file_path": file_path,
                            "status": "missing",
                            "error": "File not found"
                        })
        
        # Calculate completeness score
        if total_files > 0:
            evidence["completeness_score"] = collected_files / total_files
        
        # Generate evidence summary
        evidence["evidence_summary"] = self.generate_evidence_summary(evidence["evidence_files"])
        
        return evidence
    
    def get_file_info(self, file_path: str) -> dict:
        """Get information about a file"""
        try:
            stat = os.stat(file_path)
            file_info = {
                "file_path": file_path,
                "status": "present",
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "type": "file" if os.path.isfile(file_path) else "directory"
            }
            
            # Get additional info based on file type
            if file_path.endswith('.py'):
                file_info["lines_of_code"] = self.count_lines_of_code(file_path)
            elif file_path.endswith('.md'):
                file_info["word_count"] = self.count_words(file_path)
            elif file_path.endswith('.log'):
                file_info["log_entries"] = self.count_log_entries(file_path)
            
            return file_info
            
        except Exception as e:
            return {
                "file_path": file_path,
                "status": "error",
                "error": str(e)
            }
    
    def count_lines_of_code(self, file_path: str) -> int:
        """Count lines of code in a Python file"""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                return len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        except:
            return 0
    
    def count_words(self, file_path: str) -> int:
        """Count words in a markdown file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                return len(content.split())
        except:
            return 0
    
    def count_log_entries(self, file_path: str) -> int:
        """Count log entries in a log file"""
        try:
            with open(file_path, 'r') as f:
                return len(f.readlines())
        except:
            return 0
    
    def generate_evidence_summary(self, evidence_files: dict) -> dict:
        """Generate summary of collected evidence"""
        summary = {
            "total_files": 0,
            "present_files": 0,
            "missing_files": 0,
            "error_files": 0,
            "by_type": {}
        }
        
        for scope_area, files in evidence_files.items():
            summary["by_type"][scope_area] = {
                "total": len(files),
                "present": len([f for f in files if f["status"] == "present"]),
                "missing": len([f for f in files if f["status"] == "missing"]),
                "error": len([f for f in files if f["status"] == "error"])
            }
            
            summary["total_files"] += summary["by_type"][scope_area]["total"]
            summary["present_files"] += summary["by_type"][scope_area]["present"]
            summary["missing_files"] += summary["by_type"][scope_area]["missing"]
            summary["error_files"] += summary["by_type"][scope_area]["error"]
        
        return summary
```

#### 9.2.4.2 Audit Documentation

**Documentation Requirements:**
- **Audit Plan:** Detailed audit plan and scope
- **Audit Checklist:** Comprehensive audit checklist
- **Evidence Records:** Records of collected evidence
- **Findings Report:** Detailed findings and recommendations
- **Follow-up Actions:** Actions taken based on findings

**Current Implementation Examples:**
```python
# Audit documentation in services/audit_documentation.py
class AuditDocumentation:
    def __init__(self):
        self.documentation_templates = {
            "audit_plan": self.generate_audit_plan,
            "audit_checklist": self.generate_audit_checklist,
            "evidence_record": self.generate_evidence_record,
            "findings_report": self.generate_findings_report,
            "follow_up_actions": self.generate_follow_up_actions
        }
    
    def generate_audit_plan(self, audit_type: str, scope: list, auditor: str) -> dict:
        """Generate audit plan"""
        plan = {
            "audit_id": f"audit_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "audit_type": audit_type,
            "auditor": auditor,
            "planned_date": datetime.now().isoformat(),
            "scope": scope,
            "objectives": self.get_audit_objectives(audit_type),
            "methodology": self.get_audit_methodology(audit_type),
            "resources_required": self.get_required_resources(audit_type),
            "timeline": self.get_audit_timeline(audit_type),
            "risks": self.identify_audit_risks(audit_type)
        }
        
        return plan
    
    def generate_audit_checklist(self, audit_scope: list) -> dict:
        """Generate audit checklist"""
        checklist = {
            "checklist_id": f"checklist_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "generated_date": datetime.now().isoformat(),
            "scope": audit_scope,
            "items": []
        }
        
        for scope_area in audit_scope:
            area_items = self.get_checklist_items(scope_area)
            checklist["items"].extend(area_items)
        
        return checklist
    
    def generate_findings_report(self, audit_results: dict) -> dict:
        """Generate findings report"""
        report = {
            "report_id": f"findings_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "audit_id": audit_results.get("audit_id", "unknown"),
            "report_date": datetime.now().isoformat(),
            "executive_summary": self.generate_executive_summary(audit_results),
            "detailed_findings": audit_results.get("findings", []),
            "recommendations": audit_results.get("recommendations", []),
            "risk_assessment": self.assess_audit_risks(audit_results),
            "compliance_status": self.assess_compliance_status(audit_results),
            "next_steps": self.generate_next_steps(audit_results)
        }
        
        return report
    
    def get_audit_objectives(self, audit_type: str) -> list:
        """Get audit objectives based on audit type"""
        objectives = {
            "automated_compliance": [
                "Verify automated compliance checks are functioning",
                "Ensure performance metrics are within acceptable ranges",
                "Confirm security monitoring is active and effective"
            ],
            "comprehensive_system": [
                "Assess overall system compliance with ISO/IEC 42001:2023",
                "Evaluate effectiveness of implemented controls",
                "Identify areas for improvement and optimization"
            ],
            "iso_compliance": [
                "Verify full compliance with ISO/IEC 42001:2023 requirements",
                "Assess management system effectiveness",
                "Ensure continuous improvement processes are working"
            ]
        }
        
        return objectives.get(audit_type, [])
    
    def get_checklist_items(self, scope_area: str) -> list:
        """Get checklist items for a specific scope area"""
        checklist_items = {
            "system_performance": [
                "Verify LLM response time monitoring is active",
                "Check tool execution time tracking",
                "Validate error rate monitoring",
                "Confirm performance alert thresholds are appropriate"
            ],
            "security_compliance": [
                "Verify prompt injection detection is working",
                "Check input validation effectiveness",
                "Validate security incident response procedures",
                "Confirm audit logging is comprehensive"
            ],
            "data_management": [
                "Verify data classification procedures",
                "Check schema validation implementation",
                "Validate data retention policies",
                "Confirm privacy protection measures"
            ]
        }
        
        return checklist_items.get(scope_area, [])
```

### 9.2.5 Audit Follow-up and Corrective Actions

#### 9.2.5.1 Finding Management

**Finding Categories:**
- **Critical Findings:** Immediate action required
- **Major Findings:** Significant issues requiring attention
- **Minor Findings:** Issues that should be addressed
- **Observations:** Suggestions for improvement

**Current Implementation Examples:**
```python
# Finding management in services/finding_management.py
class FindingManagement:
    def __init__(self):
        self.finding_categories = {
            "critical": {
                "priority": 1,
                "response_time": "immediate",
                "description": "Immediate action required"
            },
            "major": {
                "priority": 2,
                "response_time": "7_days",
                "description": "Significant issues requiring attention"
            },
            "minor": {
                "priority": 3,
                "response_time": "30_days",
                "description": "Issues that should be addressed"
            },
            "observation": {
                "priority": 4,
                "response_time": "90_days",
                "description": "Suggestions for improvement"
            }
        }
        self.findings = []
    
    def add_finding(self, finding: dict) -> str:
        """Add a new finding"""
        finding_id = f"finding_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        finding.update({
            "finding_id": finding_id,
            "created_date": datetime.now().isoformat(),
            "status": "open",
            "assigned_to": None,
            "due_date": self.calculate_due_date(finding.get("category", "minor")),
            "actions_taken": [],
            "verification_date": None
        })
        
        self.findings.append(finding)
        return finding_id
    
    def calculate_due_date(self, category: str) -> str:
        """Calculate due date based on finding category"""
        category_config = self.finding_categories.get(category, self.finding_categories["minor"])
        
        if category_config["response_time"] == "immediate":
            return datetime.now().isoformat()
        elif category_config["response_time"] == "7_days":
            return (datetime.now() + timedelta(days=7)).isoformat()
        elif category_config["response_time"] == "30_days":
            return (datetime.now() + timedelta(days=30)).isoformat()
        elif category_config["response_time"] == "90_days":
            return (datetime.now() + timedelta(days=90)).isoformat()
        
        return (datetime.now() + timedelta(days=30)).isoformat()
    
    def get_findings_summary(self) -> dict:
        """Get summary of all findings"""
        summary = {
            "total_findings": len(self.findings),
            "by_category": {},
            "by_status": {},
            "overdue_findings": [],
            "critical_findings": []
        }
        
        for category in self.finding_categories:
            summary["by_category"][category] = len([f for f in self.findings if f["category"] == category])
        
        for finding in self.findings:
            status = finding.get("status", "open")
            summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
            
            # Check for overdue findings
            if finding["status"] == "open":
                due_date = datetime.fromisoformat(finding["due_date"])
                if datetime.now() > due_date:
                    summary["overdue_findings"].append(finding)
            
            # Check for critical findings
            if finding["category"] == "critical":
                summary["critical_findings"].append(finding)
        
        return summary
```

---

**Document Approval:**
- **Prepared by:** AI Management Team
- **Reviewed by:** Technical Lead
- **Approved by:** AI Management Team Lead
- **Next Review:** 2025-03-19

**References:**
- ISO/IEC 42001:2023 - Clause 9.2
- Aligned with ISO/IEC 42001:2023 - Clause 8.1
- See Control A.2.1 for governance requirements 