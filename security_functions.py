# Security Functions for ISO Compliance (R003, R001, R002)

def sanitize_prompt_input(user_input):
    """Sanitize user input to prevent prompt injection attacks (R003)"""
    if not user_input:
        return ""
    
    # Convert to string if needed
    input_str = str(user_input)
    
    # Remove or escape dangerous patterns
    dangerous_patterns = [
        "system:", "user:", "assistant:", "role:", "function:",
        "```", "'''", "<!--", "-->", "<script>", "</script>",
        "javascript:", "data:", "vbscript:", "onload=", "onerror="
    ]
    
    sanitized = input_str
    for pattern in dangerous_patterns:
        # Replace with safe alternatives
        sanitized = sanitized.replace(pattern.lower(), f"[BLOCKED_{pattern.upper().replace(':', '')}]")
        sanitized = sanitized.replace(pattern.upper(), f"[BLOCKED_{pattern.upper().replace(':', '')}]")
    
    # Limit length to prevent prompt flooding
    max_length = 1000
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "... [TRUNCATED]"
    
    return sanitized

def validate_llm_prompt(prompt):
    """Validate LLM prompt for security and compliance (R003)"""
    validation_result = {
        "is_safe": True,
        "warnings": [],
        "blocked_patterns": [],
        "recommendations": []
    }
    
    # Check for dangerous patterns
    dangerous_patterns = [
        "system:", "user:", "assistant:", "role:", "function:",
        "```", "'''", "<!--", "-->", "<script>", "</script>"
    ]
    
    for pattern in dangerous_patterns:
        if pattern.lower() in prompt.lower():
            validation_result["is_safe"] = False
            validation_result["blocked_patterns"].append(pattern)
            validation_result["warnings"].append(f"Potentially dangerous pattern: {pattern}")
    
    # Check prompt length
    if len(prompt) > 2000:
        validation_result["warnings"].append("Prompt length exceeds recommended limit")
        validation_result["recommendations"].append("Consider breaking into smaller chunks")
    
    return validation_result

def detect_bias_in_client_data(client_data):
    """Detect bias in client filtering and data (R001)"""
    bias_indicators = {
        "gender_bias": False,
        "age_bias": False,
        "geographic_bias": False,
        "economic_bias": False,
        "confidence_score": 0.0
    }
    
    try:
        # Analyze client data for bias patterns
        if isinstance(client_data, dict):
            # Check for gender bias in names
            if "name" in client_data:
                name = str(client_data["name"]).lower()
                if any(gender in name for gender in ["mr", "ms", "mrs", "dr"]):
                    bias_indicators["gender_bias"] = True
                    bias_indicators["confidence_score"] += 0.3
            
            # Check for age bias
            if "age" in client_data:
                age = client_data["age"]
                if isinstance(age, (int, float)):
                    if age < 18 or age > 80:
                        bias_indicators["age_bias"] = True
                        bias_indicators["confidence_score"] += 0.2
            
            # Check for geographic bias
            if "location" in client_data:
                location = str(client_data["location"]).lower()
                if any(region in location for region in ["north", "south", "east", "west"]):
                    bias_indicators["geographic_bias"] = True
                    bias_indicators["confidence_score"] += 0.2
    
    except Exception as e:
        pass
    
    return bias_indicators

def fact_check_llm_output(output_text, confidence_threshold=0.7):
    """Implement fact-checking layer for LLM outputs (R002)"""
    fact_check_result = {
        "is_factual": True,
        "confidence_score": 0.0,
        "warnings": [],
        "verification_method": "basic_pattern_check"
    }
    
    try:
        # Basic fact-checking patterns
        text_lower = output_text.lower()
        
        # Check for definitive statements without sources
        definitive_patterns = [
            "definitely", "certainly", "absolutely", "without a doubt",
            "proven", "fact", "truth", "reality"
        ]
        
        for pattern in definitive_patterns:
            if pattern in text_lower:
                fact_check_result["warnings"].append(f"Definitive statement: {pattern}")
                fact_check_result["confidence_score"] -= 0.1
        
        # Check for numerical claims without context
        import re
        numbers = re.findall(r"\d+", output_text)
        if len(numbers) > 3:
            fact_check_result["warnings"].append("Multiple numerical claims without context")
            fact_check_result["confidence_score"] -= 0.1
        
        # Check for source citations
        if "source:" in text_lower or "reference:" in text_lower or "according to" in text_lower:
            fact_check_result["confidence_score"] += 0.2
        
        # Calculate final confidence
        fact_check_result["confidence_score"] = max(0.0, min(1.0, fact_check_result["confidence_score"] + 0.5))
        fact_check_result["is_factual"] = fact_check_result["confidence_score"] >= confidence_threshold
        
    except Exception as e:
        fact_check_result["is_factual"] = False
        fact_check_result["confidence_score"] = 0.0
    
    return fact_check_result
