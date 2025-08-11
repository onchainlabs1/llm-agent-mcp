
# Security Functions for ISO Compliance
def sanitize_prompt_input(user_input):
    if not user_input:
        return ""
    input_str = str(user_input)
    dangerous_patterns = ["system:", "user:", "assistant:", "role:", "function:"]
    sanitized = input_str
    for pattern in dangerous_patterns:
        sanitized = sanitized.replace(pattern.lower(), "[BLOCKED]")
    return sanitized[:1000] if len(sanitized) > 1000 else sanitized

def validate_llm_prompt(prompt):
    result = {"is_safe": True, "warnings": []}
    dangerous_patterns = ["system:", "user:", "assistant:", "role:", "function:"]
    for pattern in dangerous_patterns:
        if pattern.lower() in prompt.lower():
            result["is_safe"] = False
            result["warnings"].append("Dangerous pattern detected")
    return result

def detect_bias_in_client_data(client_data):
    bias_indicators = {"gender_bias": False, "age_bias": False, "confidence_score": 0.0}
    try:
        if isinstance(client_data, dict) and "name" in client_data:
            name = str(client_data["name"]).lower()
            if any(gender in name for gender in ["mr", "ms", "mrs", "dr"]):
                bias_indicators["gender_bias"] = True
                bias_indicators["confidence_score"] += 0.3
    except:
        pass
    return bias_indicators

def fact_check_llm_output(output_text, confidence_threshold=0.7):
    result = {"is_factual": True, "confidence_score": 0.5, "warnings": []}
    try:
        text_lower = output_text.lower()
        definitive_patterns = ["definitely", "certainly", "absolutely", "proven", "fact"]
        for pattern in definitive_patterns:
            if pattern in text_lower:
                result["warnings"].append("Definitive statement detected")
                result["confidence_score"] -= 0.1
        result["confidence_score"] = max(0.0, min(1.0, result["confidence_score"]))
        result["is_factual"] = result["confidence_score"] >= confidence_threshold
    except:
        result["is_factual"] = False
        result["confidence_score"] = 0.0
    return result

