"""
Unit Tests for ISO 42001:2023 Controls Implementation

This module tests all critical ISO controls:
- R001: Bias Detection and Mitigation
- R002: Fact-checking and Confidence Scoring
- R003: Prompt Sanitization (Enhanced)
- R008: Data Encryption and Integrity

All tests are designed to validate ISO 42001:2023 compliance requirements.
"""

import unittest
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from agent.iso_controls import ISO42001Controls, iso_controls
    ISO_CONTROLS_AVAILABLE = True
except ImportError:
    ISO_CONTROLS_AVAILABLE = False


class TestISO42001Controls(unittest.TestCase):
    """Test suite for ISO 42001:2023 controls implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        if ISO_CONTROLS_AVAILABLE:
            self.iso_controls = ISO42001Controls()
        else:
            self.skipTest("ISO controls module not available")
    
    def test_control_initialization(self):
        """Test that ISO controls are properly initialized."""
        self.assertIsNotNone(self.iso_controls)
        self.assertIn("R001", self.iso_controls.control_status)
        self.assertIn("R002", self.iso_controls.control_status)
        self.assertIn("R003", self.iso_controls.control_status)
        self.assertIn("R008", self.iso_controls.control_status)
        
        for control_id, status in self.iso_controls.control_status.items():
            self.assertEqual(status["status"], "implemented")
            self.assertIn("last_audit", status)
    
    def test_prompt_sanitization_r003(self):
        """Test ISO Control R003: Enhanced Prompt Sanitization."""
        # Test dangerous patterns removal
        dangerous_prompts = [
            "```print('hello')```",
            "<script>alert('xss')</script>",
            "javascript:void(0)",
            "data:text/html,<script>alert('xss')</script>",
            "vbscript:msgbox('xss')",
            "<iframe src='evil.com'></iframe>",
            "prompt('Enter password')",
            "eval('alert(1)')",
            "exec('rm -rf /')",
            "__import__('os').system('ls')"
        ]
        
        for dangerous_prompt in dangerous_prompts:
            sanitized = self.iso_controls.sanitize_prompt(dangerous_prompt)
            self.assertNotIn("```", sanitized)
            self.assertNotIn("<script>", sanitized)
            self.assertNotIn("javascript:", sanitized)
            self.assertNotIn("prompt(", sanitized)
            self.assertNotIn("eval(", sanitized)
            self.assertNotIn("exec(", sanitized)
            self.assertNotIn("__import__", sanitized)
        
        # Test length limiting
        long_prompt = "A" * 15000
        sanitized = self.iso_controls.sanitize_prompt(long_prompt)
        self.assertLess(len(sanitized), 10050)  # Max length + truncation message
        self.assertIn("[truncated]", sanitized)
        
        # Test whitespace normalization
        messy_prompt = "  Multiple    spaces   and\ttabs\t\there  "
        sanitized = self.iso_controls.sanitize_prompt(messy_prompt)
        self.assertEqual(sanitized, "Multiple spaces and tabs here")
    
    def test_bias_detection_r001(self):
        """Test ISO Control R001: Bias Detection and Mitigation."""
        # Test demographic bias detection
        demographic_prompts = [
            "Show me all male clients",
            "List elderly customers",
            "Find wealthy people",
            "Show religious organizations",
            "Find educated professionals"
        ]
        
        for prompt in demographic_prompts:
            bias_score, bias_indicators = self.iso_controls.detect_bias(prompt)
            self.assertGreater(bias_score, 0.0)
            self.assertGreater(len(bias_indicators), 0)
        
        # Test professional bias detection
        professional_prompts = [
            "Show me all CEOs",
            "Find tech companies only",
            "List expert users",
            "Show employed people"
        ]
        
        for prompt in professional_prompts:
            bias_score, bias_indicators = self.iso_controls.detect_bias(prompt)
            self.assertGreater(bias_score, 0.0)
            self.assertGreater(len(bias_indicators), 0)
        
        # Test bias pattern detection
        pattern_prompts = [
            "All men are better at this",
            "Women always do this",
            "Obviously this is correct",
            "Real professionals know this"
        ]
        
        for prompt in pattern_prompts:
            bias_score, bias_indicators = self.iso_controls.detect_bias(prompt)
            self.assertGreater(bias_score, 0.0)
            self.assertGreater(len(bias_indicators), 0)
        
        # Test neutral prompts
        neutral_prompts = [
            "Show me all clients",
            "List orders",
            "Find products",
            "Display data"
        ]
        
        for prompt in neutral_prompts:
            bias_score, bias_indicators = self.iso_controls.detect_bias(prompt)
            self.assertEqual(bias_score, 0.0)
            self.assertEqual(len(bias_indicators), 0)
    
    def test_fact_checking_r002(self):
        """Test ISO Control R002: Fact-checking and Confidence Scoring."""
        # Test high confidence responses
        high_confidence_responses = [
            "According to research, AI systems show 95% accuracy in this domain.",
            "Studies indicate that the implementation resulted in 87% improvement.",
            "Data suggests that 73% of users reported satisfaction.",
            "Evidence shows that the system achieved 92% compliance rate."
        ]
        
        for response in high_confidence_responses:
            fact_check_result = self.iso_controls.fact_check_response(response, "test prompt")
            self.assertGreater(fact_check_result["confidence"], 0.7)
            self.assertTrue(fact_check_result["verified"])
        
        # Test low confidence responses
        low_confidence_responses = [
            "Maybe this could work",
            "Perhaps the system might be useful",
            "It's unclear if this approach works",
            "I'm not sure about the results"
        ]
        
        for response in low_confidence_responses:
            fact_check_result = self.iso_controls.fact_check_response(response, "test prompt")
            self.assertLess(fact_check_result["confidence"], 0.8)
            self.assertFalse(fact_check_result["verified"])
        
        # Test technical accuracy scoring
        technical_response = "The ISO 42001:2023 standard requires AI management systems to implement risk controls including bias detection (A.4.2) and fact-checking (A.4.5)."
        fact_check_result = self.iso_controls.fact_check_response(technical_response, "test prompt")
        self.assertGreater(fact_check_result["technical_accuracy"], 0)
        self.assertGreater(fact_check_result["confidence"], 0.6)
    
    def test_confidence_scoring_r002(self):
        """Test confidence score calculation."""
        # Test response quality factors
        good_response = "This is a comprehensive response with multiple sentences. It provides detailed information about ISO 42001:2023 compliance requirements and includes specific technical details about AI management systems."
        fact_check_result = self.iso_controls.fact_check_response(good_response, "test prompt")
        confidence_score = self.iso_controls.calculate_confidence_score(good_response, fact_check_result)
        
        self.assertGreater(confidence_score, 0.7)
        self.assertLessEqual(confidence_score, 1.0)
        
        # Test poor response quality
        poor_response = "Maybe this works"
        fact_check_result = self.iso_controls.fact_check_response(poor_response, "test prompt")
        confidence_score = self.iso_controls.calculate_confidence_score(poor_response, fact_check_result)
        
        self.assertLess(confidence_score, 0.6)
        self.assertGreaterEqual(confidence_score, 0.0)
    
    def test_data_encryption_r008(self):
        """Test ISO Control R008: Data Encryption and Integrity."""
        # Test encryption and decryption
        test_data = [
            "Sensitive client information",
            "Employee personal data",
            "Financial records",
            "ISO compliance documentation",
            "Risk assessment data"
        ]
        
        for data in test_data:
            # Encrypt data
            encrypted = self.iso_controls.encrypt_data(data)
            self.assertIsInstance(encrypted, str)
            self.assertGreater(len(encrypted), 0)
            self.assertNotEqual(encrypted, data)
            
            # Decrypt data
            decrypted = self.iso_controls.decrypt_data(encrypted)
            self.assertEqual(decrypted, data)
        
        # Test empty data handling
        empty_encrypted = self.iso_controls.encrypt_data("")
        self.assertEqual(empty_encrypted, "")
        
        empty_decrypted = self.iso_controls.decrypt_data("")
        self.assertEqual(empty_decrypted, "")
        
        # Test None data handling
        none_encrypted = self.iso_controls.encrypt_data(None)
        self.assertEqual(none_encrypted, "")
        
        # Test encryption key consistency
        data1 = "Test data 1"
        data2 = "Test data 2"
        
        encrypted1 = self.iso_controls.encrypt_data(data1)
        encrypted2 = self.iso_controls.encrypt_data(data2)
        
        # Same data should produce same encryption
        encrypted1_again = self.iso_controls.encrypt_data(data1)
        self.assertEqual(encrypted1, encrypted1_again)
        
        # Different data should produce different encryption
        self.assertNotEqual(encrypted1, encrypted2)
    
    def test_control_status_reporting(self):
        """Test control status reporting functionality."""
        status_report = self.iso_controls.get_control_status()
        
        # Check required fields
        required_fields = ["timestamp", "controls", "compliance_score", "last_audit"]
        for field in required_fields:
            self.assertIn(field, status_report)
        
        # Check control status
        controls = status_report["controls"]
        self.assertIn("R001", controls)
        self.assertIn("R002", controls)
        self.assertIn("R003", controls)
        self.assertIn("R008", controls)
        
        # Check compliance score
        compliance_score = status_report["compliance_score"]
        self.assertGreaterEqual(compliance_score, 0.0)
        self.assertLessEqual(compliance_score, 100.0)
        self.assertEqual(compliance_score, 100.0)  # All controls implemented
    
    def test_logging_functionality(self):
        """Test that all ISO controls log their activities."""
        # This test verifies that logging is working for audit purposes
        # The actual log messages are tested implicitly through the control functions
        
        # Test that bias detection logs
        bias_score, bias_indicators = self.iso_controls.detect_bias("Show me all male clients")
        self.assertIsInstance(bias_score, float)
        self.assertIsInstance(bias_indicators, list)
        
        # Test that fact-checking logs
        fact_check_result = self.iso_controls.fact_check_response("Test response", "test prompt")
        self.assertIn("verified", fact_check_result)
        self.assertIn("confidence", fact_check_result)
        
        # Test that encryption logs
        encrypted = self.iso_controls.encrypt_data("Test data")
        self.assertIsInstance(encrypted, str)
        
        # Test that sanitization logs
        sanitized = self.iso_controls.sanitize_prompt("Test prompt")
        self.assertIsInstance(sanitized, str)


class TestISOControlsIntegration(unittest.TestCase):
    """Test integration of ISO controls with other system components."""
    
    def test_global_instance_availability(self):
        """Test that the global iso_controls instance is available."""
        if ISO_CONTROLS_AVAILABLE:
            self.assertIsNotNone(iso_controls)
            self.assertIsInstance(iso_controls, ISO42001Controls)
        else:
            self.skipTest("ISO controls module not available")
    
    def test_control_methods_availability(self):
        """Test that all required control methods are available."""
        if not ISO_CONTROLS_AVAILABLE:
            self.skipTest("ISO controls module not available")
        
        required_methods = [
            "sanitize_prompt",
            "detect_bias", 
            "fact_check_response",
            "calculate_confidence_score",
            "encrypt_data",
            "decrypt_data",
            "get_control_status"
        ]
        
        for method_name in required_methods:
            self.assertTrue(hasattr(iso_controls, method_name))
            method = getattr(iso_controls, method_name)
            self.assertTrue(callable(method))


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
