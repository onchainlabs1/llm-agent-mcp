---
owner: Jennifer Park (Technical Lead)
version: 1.1
approved_by: Dr. Sarah Chen (AI System Lead)
approved_on: 2024-12-28
next_review: 2025-06-28
---

# AI Performance Monitoring and Measurement
*AI Management System - ISO/IEC 42001:2023 Compliance*

**Document Control:**
- **Document ID:** AIMS-PMM-001
- **Version:** 1.1
- **Date:** 2024-12-28
- **Status:** Approved
- **Owner:** Michael Rodriguez (AIMS Manager)

---

## 9.1 Performance Monitoring and Measurement

### 9.1.1 General

The organization shall monitor, measure, analyze, and evaluate the performance of the AI management system.

#### 9.1.1.1 Performance Monitoring Framework

The `llm-agent-mcp` project implements a comprehensive performance monitoring and measurement framework that tracks system performance, response quality, security metrics, and operational health in real-time.

### 9.1.2 Performance Metrics and KPIs

#### 9.1.2.1 Response Time Metrics

**Latency Tracking:**
- **LLM Response Time:** Time from prompt submission to LLM response
- **Tool Execution Time:** Time for MCP tool execution
- **Total Response Time:** End-to-end response time including processing
- **Interface Response Time:** Streamlit and FastAPI response times

**Current Implementation Examples:**
```python
# Performance monitoring in agent/agent_core.py
import time
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            "llm_response_times": [],
            "tool_execution_times": [],
            "total_response_times": [],
            "error_rates": [],
            "success_rates": []
        }
    
    def track_llm_response_time(self, start_time: float, end_time: float):
        """Track LLM response time"""
        response_time = end_time - start_time
        self.metrics["llm_response_times"].append({
            "timestamp": datetime.now().isoformat(),
            "response_time": response_time,
            "status": "success" if response_time < 10.0 else "slow"
        })
        
        # Log performance metric
        logger.info(f"LLM response time: {response_time:.2f}s")
        
        # Alert if response time is too high
        if response_time > 15.0:
            logger.warning(f"High LLM response time: {response_time:.2f}s")
    
    def track_tool_execution_time(self, tool_name: str, start_time: float, end_time: float):
        """Track MCP tool execution time"""
        execution_time = end_time - start_time
        self.metrics["tool_execution_times"].append({
            "timestamp": datetime.now().isoformat(),
            "tool_name": tool_name,
            "execution_time": execution_time,
            "status": "success" if execution_time < 5.0 else "slow"
        })
        
        # Log performance metric
        logger.info(f"Tool {tool_name} execution time: {execution_time:.2f}s")
        
        # Alert if execution time is too high
        if execution_time > 10.0:
            logger.warning(f"Slow tool execution: {tool_name} took {execution_time:.2f}s")
    
    def get_performance_summary(self) -> dict:
        """Get performance summary statistics"""
        summary = {
            "avg_llm_response_time": 0.0,
            "avg_tool_execution_time": 0.0,
            "total_requests": 0,
            "success_rate": 0.0,
            "error_rate": 0.0
        }
        
        if self.metrics["llm_response_times"]:
            times = [m["response_time"] for m in self.metrics["llm_response_times"]]
            summary["avg_llm_response_time"] = sum(times) / len(times)
        
        if self.metrics["tool_execution_times"]:
            times = [m["execution_time"] for m in self.metrics["tool_execution_times"]]
            summary["avg_tool_execution_time"] = sum(times) / len(times)
        
        total_requests = len(self.metrics["llm_response_times"])
        summary["total_requests"] = total_requests
        
        if total_requests > 0:
            success_count = len([m for m in self.metrics["llm_response_times"] if m["status"] == "success"])
            summary["success_rate"] = success_count / total_requests
            summary["error_rate"] = 1.0 - summary["success_rate"]
        
        return summary
```

#### 9.1.2.2 Quality Metrics

**Response Quality Assessment:**
- **Accuracy Score:** Measure of response accuracy against expected results
- **Relevance Score:** Measure of response relevance to user query
- **Completeness Score:** Measure of response completeness
- **User Satisfaction:** User feedback and satisfaction ratings

**Current Implementation Examples:**
```python
# Quality assessment in agent/agent_core.py
class QualityAssessor:
    def __init__(self):
        self.quality_metrics = {
            "accuracy_scores": [],
            "relevance_scores": [],
            "completeness_scores": [],
            "user_satisfaction": []
        }
    
    def assess_response_quality(self, user_input: str, agent_response: str, tool_result: dict) -> dict:
        """Assess the quality of agent response"""
        quality_score = {
            "accuracy": self.assess_accuracy(agent_response, tool_result),
            "relevance": self.assess_relevance(user_input, agent_response),
            "completeness": self.assess_completeness(agent_response, tool_result),
            "overall_score": 0.0
        }
        
        # Calculate overall score
        quality_score["overall_score"] = (
            quality_score["accuracy"] * 0.4 +
            quality_score["relevance"] * 0.3 +
            quality_score["completeness"] * 0.3
        )
        
        # Store metrics
        self.quality_metrics["accuracy_scores"].append(quality_score["accuracy"])
        self.quality_metrics["relevance_scores"].append(quality_score["relevance"])
        self.quality_metrics["completeness_scores"].append(quality_score["completeness"])
        
        return quality_score
    
    def assess_accuracy(self, response: str, tool_result: dict) -> float:
        """Assess response accuracy"""
        if not tool_result.get("success", False):
            return 0.0
        
        # Check if response contains expected data
        result_data = tool_result.get("result", {})
        if isinstance(result_data, dict) and result_data:
            return 1.0
        elif isinstance(result_data, list) and len(result_data) > 0:
            return 1.0
        else:
            return 0.5  # Partial accuracy
    
    def assess_relevance(self, user_input: str, response: str) -> float:
        """Assess response relevance to user input"""
        # Simple keyword matching for relevance
        input_keywords = set(user_input.lower().split())
        response_keywords = set(response.lower().split())
        
        if not input_keywords:
            return 1.0
        
        overlap = len(input_keywords.intersection(response_keywords))
        relevance = overlap / len(input_keywords)
        
        return min(relevance * 2, 1.0)  # Boost relevance score
    
    def assess_completeness(self, response: str, tool_result: dict) -> float:
        """Assess response completeness"""
        if not response or response.strip() == "":
            return 0.0
        
        # Check if response provides meaningful information
        if "no data found" in response.lower() or "error" in response.lower():
            return 0.3
        
        # Check response length and content
        if len(response) < 10:
            return 0.5
        
        return 1.0
```

### 9.1.3 Logging and Monitoring Infrastructure

#### 9.1.3.1 Structured Logging

**Log Categories:**
- **Action Logs:** All agent actions and decisions
- **Performance Logs:** Performance metrics and timing
- **Error Logs:** System errors and exceptions
- **Security Logs:** Security events and access attempts
- **Audit Logs:** Audit trail and compliance events

**Current Implementation Examples:**
```python
# Structured logging in logs/actions.log
import logging
import json
from datetime import datetime

class AIPerformanceLogger:
    def __init__(self):
        self.logger = logging.getLogger('ai_performance')
        self.logger.setLevel(logging.INFO)
        
        # File handler for performance logs
        file_handler = logging.FileHandler('logs/performance.log')
        file_handler.setLevel(logging.INFO)
        
        # JSON formatter for structured logging
        formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    def log_performance_metric(self, metric_type: str, metric_data: dict):
        """Log performance metric in structured format"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "metric_type": metric_type,
            "metric_data": metric_data,
            "log_level": "INFO"
        }
        
        self.logger.info(json.dumps(log_entry))
    
    def log_agent_action(self, action_type: str, user_input: str, agent_response: str, 
                        tool_used: str, execution_time: float, success: bool):
        """Log agent action with performance data"""
        action_log = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "user_input": user_input,
            "agent_response": agent_response,
            "tool_used": tool_used,
            "execution_time": execution_time,
            "success": success,
            "log_level": "INFO"
        }
        
        self.logger.info(json.dumps(action_log))
    
    def log_error(self, error_type: str, error_message: str, context: dict):
        """Log error with context"""
        error_log = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": error_message,
            "context": context,
            "log_level": "ERROR"
        }
        
        self.logger.error(json.dumps(error_log))
```

#### 9.1.3.2 Real-time Monitoring

**Monitoring Components:**
- **Health Checks:** System health and availability monitoring
- **Performance Alerts:** Alerts for performance degradation
- **Error Tracking:** Real-time error detection and alerting
- **Resource Monitoring:** CPU, memory, and resource usage

**Current Implementation Examples:**
```python
# Real-time monitoring in agent/agent_core.py
class RealTimeMonitor:
    def __init__(self):
        self.alert_thresholds = {
            "llm_response_time": 10.0,  # seconds
            "tool_execution_time": 5.0,  # seconds
            "error_rate": 0.05,  # 5%
            "success_rate": 0.95  # 95%
        }
        self.alerts = []
    
    def check_performance_alerts(self, metrics: dict):
        """Check for performance alerts"""
        current_alerts = []
        
        # Check LLM response time
        if metrics.get("avg_llm_response_time", 0) > self.alert_thresholds["llm_response_time"]:
            current_alerts.append({
                "type": "performance_alert",
                "metric": "llm_response_time",
                "value": metrics["avg_llm_response_time"],
                "threshold": self.alert_thresholds["llm_response_time"],
                "severity": "warning"
            })
        
        # Check tool execution time
        if metrics.get("avg_tool_execution_time", 0) > self.alert_thresholds["tool_execution_time"]:
            current_alerts.append({
                "type": "performance_alert",
                "metric": "tool_execution_time",
                "value": metrics["avg_tool_execution_time"],
                "threshold": self.alert_thresholds["tool_execution_time"],
                "severity": "warning"
            })
        
        # Check error rate
        if metrics.get("error_rate", 0) > self.alert_thresholds["error_rate"]:
            current_alerts.append({
                "type": "performance_alert",
                "metric": "error_rate",
                "value": metrics["error_rate"],
                "threshold": self.alert_thresholds["error_rate"],
                "severity": "critical"
            })
        
        # Store alerts
        self.alerts.extend(current_alerts)
        
        # Log alerts
        for alert in current_alerts:
            logger.warning(f"Performance alert: {alert['metric']} = {alert['value']} (threshold: {alert['threshold']})")
        
        return current_alerts
    
    def get_system_health(self) -> dict:
        """Get overall system health status"""
        health_status = {
            "status": "healthy",
            "alerts": len(self.alerts),
            "critical_alerts": len([a for a in self.alerts if a["severity"] == "critical"]),
            "warning_alerts": len([a for a in self.alerts if a["severity"] == "warning"]),
            "last_check": datetime.now().isoformat()
        }
        
        # Determine overall status
        if health_status["critical_alerts"] > 0:
            health_status["status"] = "critical"
        elif health_status["warning_alerts"] > 0:
            health_status["status"] = "warning"
        
        return health_status
```

### 9.1.4 Security Monitoring

#### 9.1.4.1 Prompt Injection Detection

**Detection Mechanisms:**
- **Pattern Matching:** Detection of known injection patterns
- **Behavioral Analysis:** Analysis of unusual request patterns
- **Rate Limiting:** Prevention of rapid-fire injection attempts
- **Input Validation:** Validation of input content and structure

**Current Implementation Examples:**
```python
# Security monitoring in app.py
class SecurityMonitor:
    def __init__(self):
        self.injection_patterns = [
            "ignore previous instructions",
            "system prompt",
            "you are now",
            "act as if",
            "bypass security",
            "override",
            "admin access",
            "root privileges"
        ]
        self.suspicious_requests = []
        self.blocked_ips = set()
    
    def detect_prompt_injection(self, user_input: str, user_ip: str) -> dict:
        """Detect potential prompt injection attempts"""
        detection_result = {
            "injection_detected": False,
            "patterns_found": [],
            "risk_level": "low",
            "action_taken": "none"
        }
        
        # Check for injection patterns
        for pattern in self.injection_patterns:
            if pattern.lower() in user_input.lower():
                detection_result["injection_detected"] = True
                detection_result["patterns_found"].append(pattern)
        
        # Determine risk level
        if len(detection_result["patterns_found"]) > 2:
            detection_result["risk_level"] = "high"
        elif len(detection_result["patterns_found"]) > 0:
            detection_result["risk_level"] = "medium"
        
        # Take action based on risk level
        if detection_result["risk_level"] == "high":
            detection_result["action_taken"] = "block_ip"
            self.blocked_ips.add(user_ip)
        elif detection_result["risk_level"] == "medium":
            detection_result["action_taken"] = "log_suspicious"
            self.suspicious_requests.append({
                "timestamp": datetime.now().isoformat(),
                "user_ip": user_ip,
                "user_input": user_input,
                "patterns_found": detection_result["patterns_found"]
            })
        
        # Log security event
        if detection_result["injection_detected"]:
            logger.warning(f"Prompt injection detected: {detection_result}")
        
        return detection_result
    
    def is_ip_blocked(self, user_ip: str) -> bool:
        """Check if IP is blocked"""
        return user_ip in self.blocked_ips
    
    def get_security_stats(self) -> dict:
        """Get security statistics"""
        return {
            "total_suspicious_requests": len(self.suspicious_requests),
            "blocked_ips": len(self.blocked_ips),
            "high_risk_attempts": len([r for r in self.suspicious_requests if len(r["patterns_found"]) > 2]),
            "last_security_check": datetime.now().isoformat()
        }
```

#### 9.1.4.2 Schema Validation Metrics

**Validation Tracking:**
- **Schema Compliance Rate:** Percentage of requests that pass schema validation
- **Validation Error Types:** Types and frequency of validation errors
- **Schema Update Impact:** Impact of schema changes on validation success
- **Tool Parameter Validation:** Validation of MCP tool parameters

**Current Implementation Examples:**
```python
# Schema validation monitoring in agent/tools_mcp_client.py
class SchemaValidationMonitor:
    def __init__(self):
        self.validation_metrics = {
            "total_validations": 0,
            "successful_validations": 0,
            "failed_validations": 0,
            "error_types": {},
            "tool_validation_stats": {}
        }
    
    def track_validation(self, tool_name: str, parameters: dict, validation_result: bool, error_type: str = None):
        """Track schema validation results"""
        self.validation_metrics["total_validations"] += 1
        
        if validation_result:
            self.validation_metrics["successful_validations"] += 1
        else:
            self.validation_metrics["failed_validations"] += 1
            if error_type:
                self.validation_metrics["error_types"][error_type] = \
                    self.validation_metrics["error_types"].get(error_type, 0) + 1
        
        # Track per-tool statistics
        if tool_name not in self.validation_metrics["tool_validation_stats"]:
            self.validation_metrics["tool_validation_stats"][tool_name] = {
                "total": 0,
                "successful": 0,
                "failed": 0
            }
        
        tool_stats = self.validation_metrics["tool_validation_stats"][tool_name]
        tool_stats["total"] += 1
        if validation_result:
            tool_stats["successful"] += 1
        else:
            tool_stats["failed"] += 1
    
    def get_validation_summary(self) -> dict:
        """Get validation summary statistics"""
        total = self.validation_metrics["total_validations"]
        
        summary = {
            "total_validations": total,
            "success_rate": 0.0,
            "failure_rate": 0.0,
            "most_common_errors": [],
            "tool_performance": {}
        }
        
        if total > 0:
            summary["success_rate"] = self.validation_metrics["successful_validations"] / total
            summary["failure_rate"] = self.validation_metrics["failed_validations"] / total
        
        # Get most common error types
        error_types = self.validation_metrics["error_types"]
        if error_types:
            sorted_errors = sorted(error_types.items(), key=lambda x: x[1], reverse=True)
            summary["most_common_errors"] = sorted_errors[:5]
        
        # Get tool performance
        for tool_name, stats in self.validation_metrics["tool_validation_stats"].items():
            if stats["total"] > 0:
                summary["tool_performance"][tool_name] = {
                    "success_rate": stats["successful"] / stats["total"],
                    "total_attempts": stats["total"]
                }
        
        return summary
```

### 9.1.5 Error Logging Pipeline

#### 9.1.5.1 Error Classification

**Error Categories:**
- **LLM Errors:** Errors from LLM API calls
- **MCP Protocol Errors:** Errors in MCP tool execution
- **Schema Validation Errors:** Errors in data validation
- **System Errors:** General system and infrastructure errors
- **User Input Errors:** Errors related to user input processing

**Current Implementation Examples:**
```python
# Error logging pipeline in agent/agent_core.py
class ErrorLogger:
    def __init__(self):
        self.error_categories = {
            "llm_errors": [],
            "mcp_errors": [],
            "schema_errors": [],
            "system_errors": [],
            "user_input_errors": []
        }
    
    def log_error(self, error_category: str, error_message: str, context: dict, severity: str = "medium"):
        """Log error with categorization and context"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "category": error_category,
            "message": error_message,
            "context": context,
            "severity": severity,
            "stack_trace": self.get_stack_trace()
        }
        
        # Store in appropriate category
        if error_category in self.error_categories:
            self.error_categories[error_category].append(error_entry)
        
        # Log to file
        logger.error(json.dumps(error_entry))
        
        # Alert for critical errors
        if severity == "critical":
            self.send_critical_alert(error_entry)
    
    def get_error_summary(self) -> dict:
        """Get error summary statistics"""
        summary = {
            "total_errors": 0,
            "errors_by_category": {},
            "errors_by_severity": {},
            "recent_errors": []
        }
        
        # Count errors by category
        for category, errors in self.error_categories.items():
            summary["errors_by_category"][category] = len(errors)
            summary["total_errors"] += len(errors)
        
        # Count errors by severity
        for category, errors in self.error_categories.items():
            for error in errors:
                severity = error["severity"]
                summary["errors_by_severity"][severity] = \
                    summary["errors_by_severity"].get(severity, 0) + 1
        
        # Get recent errors (last 10)
        all_errors = []
        for errors in self.error_categories.values():
            all_errors.extend(errors)
        
        all_errors.sort(key=lambda x: x["timestamp"], reverse=True)
        summary["recent_errors"] = all_errors[:10]
        
        return summary
    
    def get_stack_trace(self) -> str:
        """Get current stack trace"""
        import traceback
        return traceback.format_exc()
    
    def send_critical_alert(self, error_entry: dict):
        """Send critical error alert"""
        alert_message = {
            "type": "critical_error_alert",
            "error": error_entry,
            "timestamp": datetime.now().isoformat()
        }
        
        # Log critical alert
        logger.critical(json.dumps(alert_message))
        
        # In a production environment, this would send to monitoring system
        # For now, just log the alert
        print(f"CRITICAL ERROR ALERT: {error_entry['message']}")
```

### 9.1.6 Performance Dashboards and Reporting

#### 9.1.6.1 Real-time Dashboards

**Dashboard Components:**
- **Performance Metrics:** Real-time performance indicators
- **Error Rates:** Current error rates and trends
- **Security Alerts:** Active security alerts and threats
- **System Health:** Overall system health status

**Current Implementation Examples:**
```python
# Performance dashboard in api/routers/health.py
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/performance-dashboard")
def get_performance_dashboard():
    """Get real-time performance dashboard data"""
    try:
        # Get performance metrics
        performance_monitor = PerformanceMonitor()
        quality_assessor = QualityAssessor()
        security_monitor = SecurityMonitor()
        schema_monitor = SchemaValidationMonitor()
        error_logger = ErrorLogger()
        
        dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "performance": performance_monitor.get_performance_summary(),
            "quality": {
                "avg_accuracy": sum(quality_assessor.quality_metrics["accuracy_scores"]) / 
                               len(quality_assessor.quality_metrics["accuracy_scores"]) if quality_assessor.quality_metrics["accuracy_scores"] else 0,
                "avg_relevance": sum(quality_assessor.quality_metrics["relevance_scores"]) / 
                                len(quality_assessor.quality_metrics["relevance_scores"]) if quality_assessor.quality_metrics["relevance_scores"] else 0,
                "avg_completeness": sum(quality_assessor.quality_metrics["completeness_scores"]) / 
                                   len(quality_assessor.quality_metrics["completeness_scores"]) if quality_assessor.quality_metrics["completeness_scores"] else 0
            },
            "security": security_monitor.get_security_stats(),
            "validation": schema_monitor.get_validation_summary(),
            "errors": error_logger.get_error_summary(),
            "system_health": "healthy"  # Would be determined by health checks
        }
        
        return dashboard_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating dashboard: {str(e)}")

@router.get("/performance-metrics")
def get_performance_metrics():
    """Get detailed performance metrics"""
    try:
        performance_monitor = PerformanceMonitor()
        return performance_monitor.get_performance_summary()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting metrics: {str(e)}")

@router.get("/error-summary")
def get_error_summary():
    """Get error summary"""
    try:
        error_logger = ErrorLogger()
        return error_logger.get_error_summary()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting error summary: {str(e)}")
```

#### 9.1.6.2 Automated Reporting

**Report Types:**
- **Daily Performance Reports:** Daily performance summaries
- **Weekly Trend Reports:** Weekly performance trends
- **Monthly Compliance Reports:** Monthly compliance summaries
- **Incident Reports:** Reports on security incidents and errors

**Current Implementation Examples:**
```python
# Automated reporting in services/reporting.py
class AutomatedReporter:
    def __init__(self):
        self.report_templates = {
            "daily": self.generate_daily_report,
            "weekly": self.generate_weekly_report,
            "monthly": self.generate_monthly_report
        }
    
    def generate_daily_report(self) -> dict:
        """Generate daily performance report"""
        performance_monitor = PerformanceMonitor()
        security_monitor = SecurityMonitor()
        error_logger = ErrorLogger()
        
        report = {
            "report_type": "daily",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "performance_summary": performance_monitor.get_performance_summary(),
            "security_summary": security_monitor.get_security_stats(),
            "error_summary": error_logger.get_error_summary(),
            "recommendations": self.generate_recommendations()
        }
        
        # Save report
        self.save_report(report)
        
        return report
    
    def generate_weekly_report(self) -> dict:
        """Generate weekly performance report"""
        # Aggregate daily data for the week
        weekly_data = self.aggregate_weekly_data()
        
        report = {
            "report_type": "weekly",
            "week_start": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "week_end": datetime.now().strftime("%Y-%m-%d"),
            "weekly_trends": weekly_data,
            "performance_analysis": self.analyze_weekly_performance(weekly_data),
            "recommendations": self.generate_weekly_recommendations(weekly_data)
        }
        
        return report
    
    def generate_recommendations(self) -> list:
        """Generate recommendations based on current metrics"""
        recommendations = []
        
        # Get current metrics
        performance_monitor = PerformanceMonitor()
        metrics = performance_monitor.get_performance_summary()
        
        # Generate recommendations based on metrics
        if metrics.get("avg_llm_response_time", 0) > 8.0:
            recommendations.append("Consider optimizing LLM prompts or switching to faster model")
        
        if metrics.get("error_rate", 0) > 0.05:
            recommendations.append("Investigate and fix high error rate issues")
        
        if metrics.get("success_rate", 0) < 0.95:
            recommendations.append("Review and improve system reliability")
        
        return recommendations
    
    def save_report(self, report: dict):
        """Save report to file"""
        filename = f"reports/{report['report_type']}_{report.get('date', datetime.now().strftime('%Y-%m-%d'))}.json"
        
        # Ensure reports directory exists
        import os
        os.makedirs("reports", exist_ok=True)
        
        # Save report
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
```

### 9.1.7 Continuous Monitoring Integration

#### 9.1.7.1 Streamlit Integration

**Real-time Monitoring in UI:**
- **Performance Indicators:** Display current performance metrics
- **Error Alerts:** Show active error alerts
- **Security Status:** Display security monitoring status
- **System Health:** Show overall system health

**Current Implementation Examples:**
```python
# Streamlit monitoring integration in app.py
def display_performance_metrics():
    """Display performance metrics in Streamlit sidebar"""
    st.sidebar.header("📊 Performance Metrics")
    
    # Get current metrics
    try:
        performance_monitor = PerformanceMonitor()
        metrics = performance_monitor.get_performance_summary()
        
        # Display key metrics
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            st.metric("Avg Response Time", f"{metrics.get('avg_llm_response_time', 0):.2f}s")
            st.metric("Success Rate", f"{metrics.get('success_rate', 0)*100:.1f}%")
        
        with col2:
            st.metric("Total Requests", metrics.get('total_requests', 0))
            st.metric("Error Rate", f"{metrics.get('error_rate', 0)*100:.1f}%")
        
        # Display system health
        real_time_monitor = RealTimeMonitor()
        health = real_time_monitor.get_system_health()
        
        if health["status"] == "healthy":
            st.sidebar.success("🟢 System Healthy")
        elif health["status"] == "warning":
            st.sidebar.warning("🟡 System Warning")
        else:
            st.sidebar.error("🔴 System Critical")
        
        # Show active alerts
        if health["alerts"] > 0:
            st.sidebar.warning(f"⚠️ {health['alerts']} Active Alerts")
            
    except Exception as e:
        st.sidebar.error(f"Error loading metrics: {str(e)}")

def display_security_status():
    """Display security status in Streamlit"""
    st.sidebar.header("🛡️ Security Status")
    
    try:
        security_monitor = SecurityMonitor()
        security_stats = security_monitor.get_security_stats()
        
        st.sidebar.metric("Suspicious Requests", security_stats.get("total_suspicious_requests", 0))
        st.sidebar.metric("Blocked IPs", security_stats.get("blocked_ips", 0))
        
        if security_stats.get("high_risk_attempts", 0) > 0:
            st.sidebar.error(f"🚨 {security_stats['high_risk_attempts']} High Risk Attempts")
            
    except Exception as e:
        st.sidebar.error(f"Error loading security status: {str(e)}")
```

---

**Document Approval:**
- **Prepared by:** Michael Rodriguez (AIMS Manager)
- **Reviewed by:** Technical Lead
- **Approved by:** Dr. Sarah Chen (AI System Lead)
- **Next Review:** 2025-06-28

**References:**
- ISO/IEC 42001:2023 - Clause 9.1
- Aligned with ISO/IEC 42001:2023 - Clause 8.1
- See Control A.2.1 for governance requirements 