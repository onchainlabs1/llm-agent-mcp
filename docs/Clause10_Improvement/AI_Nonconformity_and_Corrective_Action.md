# AI Nonconformity and Corrective Action
*AI Management System - ISO/IEC 42001:2023 Compliance*

**Document Control:**
- **Document ID:** AIMS-NCA-001
- **Version:** 1.1
- **Date:** 2024-12-28
- **Status:** Approved
- **Owner:** Michael Rodriguez (AIMS Manager)

---

## 10.1 Nonconformity and Corrective Action

### 10.1.1 General

The organization shall react to nonconformities and take action to control and correct them and deal with the consequences.

#### 10.1.1.1 Nonconformity Management Framework

The `llm-agent-mcp` project implements a comprehensive nonconformity management framework that ensures systematic identification, analysis, correction, and prevention of nonconformities through integrated tools and processes.

### 10.1.2 Nonconformity Identification

#### 10.1.2.1 Identification Sources

**Primary Identification Sources:**
- **Automated Testing:** CI/CD pipeline failures and test results
- **Code Quality Checks:** Linting, security scanning, and dependency analysis
- **Performance Monitoring:** Performance threshold breaches and alerts
- **Security Monitoring:** Security incidents and vulnerability detections
- **User Feedback:** Bug reports and user complaints
- **Audit Findings:** Internal and external audit results
- **Compliance Checks:** ISO/IEC 42001:2023 compliance gaps

**Current Implementation Examples:**
```python
# Nonconformity identification in services/nonconformity_detection.py
from datetime import datetime
import logging

class NonconformityDetector:
    def __init__(self):
        self.detection_sources = {
            "automated_testing": self.detect_test_failures,
            "code_quality": self.detect_code_quality_issues,
            "performance_monitoring": self.detect_performance_issues,
            "security_monitoring": self.detect_security_issues,
            "user_feedback": self.detect_user_issues,
            "audit_findings": self.detect_audit_issues,
            "compliance_checks": self.detect_compliance_issues
        }
        self.logger = logging.getLogger('nonconformity_detection')
    
    def detect_all_nonconformities(self) -> dict:
        """Detect nonconformities from all sources"""
        nonconformities = {
            "detection_date": datetime.now().isoformat(),
            "total_nonconformities": 0,
            "by_source": {},
            "by_severity": {},
            "by_category": {}
        }
        
        for source_name, detection_method in self.detection_sources.items():
            try:
                source_nonconformities = detection_method()
                nonconformities["by_source"][source_name] = source_nonconformities
                nonconformities["total_nonconformities"] += len(source_nonconformities)
                
                # Categorize by severity and category
                for nc in source_nonconformities:
                    severity = nc.get("severity", "medium")
                    category = nc.get("category", "general")
                    
                    nonconformities["by_severity"][severity] = \
                        nonconformities["by_severity"].get(severity, 0) + 1
                    nonconformities["by_category"][category] = \
                        nonconformities["by_category"].get(category, 0) + 1
                        
            except Exception as e:
                self.logger.error(f"Error detecting nonconformities from {source_name}: {str(e)}")
        
        return nonconformities
    
    def detect_test_failures(self) -> list:
        """Detect nonconformities from automated testing"""
        nonconformities = []
        
        # This would read from actual test results
        # For now, we'll provide a framework
        test_failures = [
            {
                "test_id": "test_001",
                "test_name": "test_agent_response_time",
                "failure_type": "performance",
                "description": "Agent response time exceeds threshold",
                "severity": "high",
                "category": "performance",
                "detected_at": datetime.now().isoformat()
            },
            {
                "test_id": "test_002",
                "test_name": "test_security_validation",
                "failure_type": "security",
                "description": "Security validation test failed",
                "severity": "critical",
                "category": "security",
                "detected_at": datetime.now().isoformat()
            }
        ]
        
        for failure in test_failures:
            nonconformities.append({
                "nonconformity_id": f"nc_test_{failure['test_id']}",
                "source": "automated_testing",
                "title": f"Test Failure: {failure['test_name']}",
                "description": failure["description"],
                "severity": failure["severity"],
                "category": failure["category"],
                "detected_at": failure["detected_at"],
                "status": "open"
            })
        
        return nonconformities
    
    def detect_code_quality_issues(self) -> list:
        """Detect nonconformities from code quality checks"""
        nonconformities = []
        
        # This would read from flake8, bandit, or other code quality tools
        quality_issues = [
            {
                "file": "agent/agent_core.py",
                "line": 45,
                "issue_type": "flake8",
                "description": "E501 line too long (120 > 79 characters)",
                "severity": "low",
                "category": "code_quality"
            },
            {
                "file": "app.py",
                "line": 23,
                "issue_type": "bandit",
                "description": "B101: Use of assert detected",
                "severity": "medium",
                "category": "security"
            }
        ]
        
        for issue in quality_issues:
            nonconformities.append({
                "nonconformity_id": f"nc_quality_{issue['file'].replace('/', '_')}_{issue['line']}",
                "source": "code_quality",
                "title": f"Code Quality Issue: {issue['issue_type']}",
                "description": f"{issue['description']} in {issue['file']}:{issue['line']}",
                "severity": issue["severity"],
                "category": issue["category"],
                "detected_at": datetime.now().isoformat(),
                "status": "open"
            })
        
        return nonconformities
    
    def detect_performance_issues(self) -> list:
        """Detect nonconformities from performance monitoring"""
        nonconformities = []
        
        # This would read from performance monitoring data
        performance_thresholds = {
            "llm_response_time": 10.0,  # seconds
            "tool_execution_time": 5.0,  # seconds
            "error_rate": 0.05,  # 5%
            "success_rate": 0.95  # 95%
        }
        
        # Simulate performance issues
        current_metrics = {
            "llm_response_time": 12.5,
            "tool_execution_time": 6.2,
            "error_rate": 0.08,
            "success_rate": 0.92
        }
        
        for metric, threshold in performance_thresholds.items():
            current_value = current_metrics.get(metric, 0)
            
            if metric in ["llm_response_time", "tool_execution_time"]:
                if current_value > threshold:
                    nonconformities.append({
                        "nonconformity_id": f"nc_perf_{metric}",
                        "source": "performance_monitoring",
                        "title": f"Performance Issue: {metric}",
                        "description": f"{metric} exceeds threshold: {current_value} > {threshold}",
                        "severity": "high",
                        "category": "performance",
                        "detected_at": datetime.now().isoformat(),
                        "status": "open"
                    })
            elif metric in ["error_rate"]:
                if current_value > threshold:
                    nonconformities.append({
                        "nonconformity_id": f"nc_perf_{metric}",
                        "source": "performance_monitoring",
                        "title": f"Performance Issue: {metric}",
                        "description": f"{metric} exceeds threshold: {current_value} > {threshold}",
                        "severity": "critical",
                        "category": "reliability",
                        "detected_at": datetime.now().isoformat(),
                        "status": "open"
                    })
            elif metric in ["success_rate"]:
                if current_value < threshold:
                    nonconformities.append({
                        "nonconformity_id": f"nc_perf_{metric}",
                        "source": "performance_monitoring",
                        "title": f"Performance Issue: {metric}",
                        "description": f"{metric} below threshold: {current_value} < {threshold}",
                        "severity": "critical",
                        "category": "reliability",
                        "detected_at": datetime.now().isoformat(),
                        "status": "open"
                    })
        
        return nonconformities
```

#### 10.1.2.2 GitHub Integration

**GitHub Issues Integration:**
- **Automatic Issue Creation:** Nonconformities automatically create GitHub issues
- **Issue Templates:** Standardized templates for different nonconformity types
- **Labeling System:** Automatic labeling by severity, category, and source
- **Assignment:** Automatic assignment to appropriate team members

**Current Implementation Examples:**
```python
# GitHub integration in services/github_integration.py
import requests
import json

class GitHubIntegration:
    def __init__(self, repo_owner: str, repo_name: str, token: str):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = token
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def create_nonconformity_issue(self, nonconformity: dict) -> dict:
        """Create a GitHub issue for a nonconformity"""
        issue_data = {
            "title": f"[NONCONFORMITY] {nonconformity['title']}",
            "body": self.generate_issue_body(nonconformity),
            "labels": self.generate_issue_labels(nonconformity),
            "assignees": self.determine_assignees(nonconformity)
        }
        
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/issues"
        
        try:
            response = requests.post(url, headers=self.headers, json=issue_data)
            response.raise_for_status()
            
            issue = response.json()
            
            # Update nonconformity with GitHub issue info
            nonconformity["github_issue"] = {
                "issue_number": issue["number"],
                "issue_url": issue["html_url"],
                "created_at": issue["created_at"]
            }
            
            return nonconformity
            
        except Exception as e:
            raise Exception(f"Failed to create GitHub issue: {str(e)}")
    
    def generate_issue_body(self, nonconformity: dict) -> str:
        """Generate issue body from nonconformity data"""
        body = f"""
## Nonconformity Details

**ID:** {nonconformity['nonconformity_id']}
**Source:** {nonconformity['source']}
**Severity:** {nonconformity['severity']}
**Category:** {nonconformity['category']}
**Detected:** {nonconformity['detected_at']}

## Description
{nonconformity['description']}

## Required Actions
- [ ] Root cause analysis
- [ ] Corrective action planning
- [ ] Implementation
- [ ] Verification
- [ ] Documentation update

## Related Files
{self.identify_related_files(nonconformity)}

## Notes
*This issue was automatically created by the nonconformity detection system.*
        """.strip()
        
        return body
    
    def generate_issue_labels(self, nonconformity: dict) -> list:
        """Generate labels for the GitHub issue"""
        labels = [
            "nonconformity",
            f"severity-{nonconformity['severity']}",
            f"category-{nonconformity['category']}",
            f"source-{nonconformity['source']}"
        ]
        
        # Add priority labels based on severity
        severity_priority = {
            "critical": "priority-high",
            "high": "priority-medium",
            "medium": "priority-low",
            "low": "priority-low"
        }
        
        labels.append(severity_priority.get(nonconformity["severity"], "priority-low"))
        
        return labels
    
    def determine_assignees(self, nonconformity: dict) -> list:
        """Determine appropriate assignees based on nonconformity type"""
        assignees = []
        
        # Assign based on category
        category_assignees = {
            "security": ["security-team"],
            "performance": ["performance-team"],
            "code_quality": ["development-team"],
            "compliance": ["compliance-team"],
            "reliability": ["operations-team"]
        }
        
        category = nonconformity.get("category", "general")
        if category in category_assignees:
            assignees.extend(category_assignees[category])
        
        # Assign based on severity
        if nonconformity.get("severity") == "critical":
            assignees.append("ai-management-team")
        
        return assignees
```

### 10.1.3 Root Cause Analysis

#### 10.1.3.1 Analysis Methods

**Analysis Techniques:**
- **5 Whys Analysis:** Systematic questioning to identify root causes
- **Fishbone Diagram:** Visual analysis of cause-and-effect relationships
- **Fault Tree Analysis:** Logical analysis of failure modes
- **Process Mapping:** Analysis of process-related nonconformities

**Current Implementation Examples:**
```python
# Root cause analysis in services/root_cause_analysis.py
class RootCauseAnalyzer:
    def __init__(self):
        self.analysis_methods = {
            "5_whys": self.perform_5_whys_analysis,
            "fishbone": self.perform_fishbone_analysis,
            "fault_tree": self.perform_fault_tree_analysis,
            "process_mapping": self.perform_process_mapping
        }
    
    def analyze_root_cause(self, nonconformity: dict) -> dict:
        """Perform root cause analysis for a nonconformity"""
        analysis = {
            "nonconformity_id": nonconformity["nonconformity_id"],
            "analysis_date": datetime.now().isoformat(),
            "analysis_method": self.select_analysis_method(nonconformity),
            "root_causes": [],
            "contributing_factors": [],
            "analysis_notes": "",
            "confidence_level": 0.0
        }
        
        # Perform analysis based on selected method
        method = analysis["analysis_method"]
        if method in self.analysis_methods:
            analysis_result = self.analysis_methods[method](nonconformity)
            analysis.update(analysis_result)
        
        return analysis
    
    def perform_5_whys_analysis(self, nonconformity: dict) -> dict:
        """Perform 5 Whys analysis"""
        analysis_result = {
            "root_causes": [],
            "contributing_factors": [],
            "analysis_notes": ""
        }
        
        # Example 5 Whys analysis for performance issue
        if nonconformity["category"] == "performance":
            why_chain = [
                "Why is the response time slow?",
                "Because the LLM API call is taking too long",
                "Why is the LLM API call slow?",
                "Because we're using a large model for simple queries",
                "Why are we using a large model?",
                "Because the model selection logic doesn't consider query complexity",
                "Why doesn't the selection logic consider complexity?",
                "Because the complexity assessment algorithm is not implemented"
            ]
            
            analysis_result["root_causes"].append("Missing query complexity assessment")
            analysis_result["contributing_factors"].extend([
                "Large model selection for simple queries",
                "Inefficient model selection logic"
            ])
            analysis_result["analysis_notes"] = "5 Whys analysis completed - root cause identified"
        
        return analysis_result
    
    def select_analysis_method(self, nonconformity: dict) -> str:
        """Select appropriate analysis method based on nonconformity type"""
        category_methods = {
            "performance": "5_whys",
            "security": "fault_tree",
            "process": "process_mapping",
            "code_quality": "5_whys",
            "reliability": "fishbone"
        }
        
        return category_methods.get(nonconformity.get("category", "general"), "5_whys")
```

### 10.1.4 Corrective Action Planning

#### 10.1.4.1 Action Planning Process

**Planning Steps:**
- **Action Identification:** Identify specific corrective actions
- **Resource Assessment:** Assess required resources and capabilities
- **Timeline Planning:** Develop implementation timeline
- **Risk Assessment:** Assess risks of corrective actions
- **Success Criteria:** Define success criteria for verification

**Current Implementation Examples:**
```python
# Corrective action planning in services/corrective_action_planning.py
class CorrectiveActionPlanner:
    def __init__(self):
        self.action_templates = {
            "performance": self.generate_performance_actions,
            "security": self.generate_security_actions,
            "code_quality": self.generate_code_quality_actions,
            "reliability": self.generate_reliability_actions
        }
    
    def plan_corrective_actions(self, nonconformity: dict, root_cause_analysis: dict) -> dict:
        """Plan corrective actions for a nonconformity"""
        plan = {
            "nonconformity_id": nonconformity["nonconformity_id"],
            "plan_date": datetime.now().isoformat(),
            "actions": [],
            "timeline": {},
            "resources": {},
            "risks": [],
            "success_criteria": []
        }
        
        # Generate actions based on category
        category = nonconformity.get("category", "general")
        if category in self.action_templates:
            actions = self.action_templates[category](nonconformity, root_cause_analysis)
            plan["actions"] = actions
        
        # Plan timeline
        plan["timeline"] = self.plan_implementation_timeline(plan["actions"])
        
        # Assess resources
        plan["resources"] = self.assess_resource_requirements(plan["actions"])
        
        # Identify risks
        plan["risks"] = self.assess_implementation_risks(plan["actions"])
        
        # Define success criteria
        plan["success_criteria"] = self.define_success_criteria(nonconformity, plan["actions"])
        
        return plan
    
    def generate_performance_actions(self, nonconformity: dict, analysis: dict) -> list:
        """Generate corrective actions for performance issues"""
        actions = []
        
        if "Missing query complexity assessment" in analysis.get("root_causes", []):
            actions.extend([
                {
                    "action_id": f"action_{datetime.now().strftime('%Y%m%d_%H%M%S')}_1",
                    "description": "Implement query complexity assessment algorithm",
                    "type": "development",
                    "priority": "high",
                    "estimated_effort": "2_days",
                    "assigned_to": "development-team"
                },
                {
                    "action_id": f"action_{datetime.now().strftime('%Y%m%d_%H%M%S')}_2",
                    "description": "Update model selection logic to use complexity assessment",
                    "type": "development",
                    "priority": "high",
                    "estimated_effort": "1_day",
                    "assigned_to": "development-team"
                },
                {
                    "action_id": f"action_{datetime.now().strftime('%Y%m%d_%H%M%S')}_3",
                    "description": "Add performance monitoring for model selection",
                    "type": "monitoring",
                    "priority": "medium",
                    "estimated_effort": "0.5_days",
                    "assigned_to": "operations-team"
                }
            ])
        
        return actions
    
    def plan_implementation_timeline(self, actions: list) -> dict:
        """Plan implementation timeline for actions"""
        timeline = {
            "total_duration": "0_days",
            "critical_path": [],
            "milestones": []
        }
        
        if actions:
            # Calculate total duration
            total_effort = 0
            for action in actions:
                effort = action.get("estimated_effort", "0_days")
                if "days" in effort:
                    days = float(effort.replace("_days", ""))
                    total_effort += days
            
            timeline["total_duration"] = f"{total_effort}_days"
            
            # Identify critical path
            high_priority_actions = [a for a in actions if a.get("priority") == "high"]
            timeline["critical_path"] = [a["action_id"] for a in high_priority_actions]
            
            # Define milestones
            timeline["milestones"] = [
                {
                    "milestone": "Analysis Complete",
                    "date": datetime.now().isoformat(),
                    "status": "completed"
                },
                {
                    "milestone": "Implementation Start",
                    "date": (datetime.now() + timedelta(days=1)).isoformat(),
                    "status": "planned"
                },
                {
                    "milestone": "Implementation Complete",
                    "date": (datetime.now() + timedelta(days=total_effort)).isoformat(),
                    "status": "planned"
                }
            ]
        
        return timeline
```

### 10.1.5 Implementation and Tracking

#### 10.1.5.1 Implementation Process

**Implementation Steps:**
- **Action Assignment:** Assign actions to responsible parties
- **Progress Tracking:** Track implementation progress
- **Quality Assurance:** Ensure implementation quality
- **Documentation:** Update relevant documentation

**Current Implementation Examples:**
```python
# Implementation tracking in services/implementation_tracking.py
class ImplementationTracker:
    def __init__(self):
        self.implementations = []
        self.statuses = ["planned", "in_progress", "completed", "verified", "closed"]
    
    def start_implementation(self, action: dict) -> dict:
        """Start implementation of a corrective action"""
        implementation = {
            "action_id": action["action_id"],
            "start_date": datetime.now().isoformat(),
            "status": "in_progress",
            "progress_updates": [],
            "completion_date": None,
            "verification_date": None,
            "documentation_updates": []
        }
        
        self.implementations.append(implementation)
        return implementation
    
    def update_progress(self, action_id: str, progress: str, notes: str = None) -> bool:
        """Update implementation progress"""
        for impl in self.implementations:
            if impl["action_id"] == action_id:
                impl["progress_updates"].append({
                    "date": datetime.now().isoformat(),
                    "progress": progress,
                    "notes": notes
                })
                
                if progress == "completed":
                    impl["status"] = "completed"
                    impl["completion_date"] = datetime.now().isoformat()
                
                return True
        
        return False
    
    def verify_implementation(self, action_id: str, verification_data: dict) -> dict:
        """Verify implementation effectiveness"""
        verification = {
            "action_id": action_id,
            "verification_date": datetime.now().isoformat(),
            "verification_method": verification_data.get("method", "testing"),
            "success_criteria_met": verification_data.get("success", False),
            "verification_notes": verification_data.get("notes", ""),
            "next_steps": verification_data.get("next_steps", [])
        }
        
        # Update implementation status
        for impl in self.implementations:
            if impl["action_id"] == action_id:
                impl["verification_date"] = verification["verification_date"]
                if verification["success_criteria_met"]:
                    impl["status"] = "verified"
                else:
                    impl["status"] = "in_progress"
                break
        
        return verification
```

### 10.1.6 Documentation and Records

#### 10.1.6.1 Documentation Requirements

**Documentation Elements:**
- **Nonconformity Records:** Complete records of nonconformities
- **Root Cause Analysis:** Analysis results and findings
- **Corrective Actions:** Action plans and implementation details
- **Verification Results:** Results of corrective action verification
- **Lessons Learned:** Lessons learned from nonconformity resolution

**Current Implementation Examples:**
```python
# Documentation management in services/documentation_management.py
class NonconformityDocumentation:
    def __init__(self):
        self.documentation_structure = {
            "nonconformity_records": "docs/nonconformities/",
            "root_cause_analyses": "docs/analyses/",
            "corrective_actions": "docs/actions/",
            "verification_results": "docs/verifications/",
            "lessons_learned": "docs/lessons/"
        }
    
    def document_nonconformity(self, nonconformity: dict, analysis: dict, plan: dict) -> dict:
        """Document complete nonconformity resolution"""
        documentation = {
            "nonconformity_id": nonconformity["nonconformity_id"],
            "documentation_date": datetime.now().isoformat(),
            "nonconformity_record": self.create_nonconformity_record(nonconformity),
            "root_cause_analysis": self.create_analysis_record(analysis),
            "corrective_action_plan": self.create_action_record(plan),
            "verification_results": None,  # Will be added after verification
            "lessons_learned": None,  # Will be added after completion
            "documentation_status": "in_progress"
        }
        
        return documentation
    
    def create_nonconformity_record(self, nonconformity: dict) -> dict:
        """Create nonconformity record"""
        return {
            "id": nonconformity["nonconformity_id"],
            "title": nonconformity["title"],
            "description": nonconformity["description"],
            "source": nonconformity["source"],
            "severity": nonconformity["severity"],
            "category": nonconformity["category"],
            "detected_at": nonconformity["detected_at"],
            "status": nonconformity["status"],
            "github_issue": nonconformity.get("github_issue", {})
        }
    
    def update_documentation(self, nonconformity_id: str, updates: dict) -> bool:
        """Update documentation with new information"""
        # This would update the actual documentation files
        # For now, we'll provide a framework
        update_types = {
            "verification_results": self.update_verification_results,
            "lessons_learned": self.update_lessons_learned,
            "implementation_progress": self.update_implementation_progress
        }
        
        for update_type, update_data in updates.items():
            if update_type in update_types:
                update_types[update_type](nonconformity_id, update_data)
        
        return True
```

---

**Document Approval:**
- **Prepared by:** Michael Rodriguez (AIMS Manager)
- **Reviewed by:** Technical Lead
- **Approved by:** Dr. Sarah Chen (AI System Lead)
- **Next Review:** 2025-06-28

**References:**
- ISO/IEC 42001:2023 - Clause 10.1
- Aligned with ISO/IEC 42001:2023 - Clause 9.2
- See Control A.2.1 for governance requirements 