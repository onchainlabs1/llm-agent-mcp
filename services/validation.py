"""
Input validation and sanitization utilities for AgentMCP services.

This module provides utilities for validating and sanitizing user input
to prevent injection attacks and ensure data integrity.
"""

import html
import json
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional, Union

from email_validator import EmailNotValidError, validate_email
from pydantic import ValidationError as PydanticValidationError

from .models import (
    ClientCreate,
    ClientSearchFilter,
    ClientUpdate,
    EmployeeCreate,
    EmployeeSearchFilter,
    OrderCreate,
    ValidationError,
)


class InputValidator:
    """Input validation and sanitization utilities."""

    # Regular expressions for common validations
    PHONE_REGEX = re.compile(r"^\+?[\d\s\-\(\)]{10,20}$")
    CLIENT_ID_REGEX = re.compile(r"^[a-zA-Z0-9\-_]{1,100}$")
    NAME_REGEX = re.compile(
        r"^[a-zA-Z\s\-\.\'\u00C0-\u017F]{1,200}$"
    )  # Allow accented characters
    SAFE_STRING_REGEX = re.compile(r"^[a-zA-Z0-9\s\-_.,@#()]*$")

    @classmethod
    def sanitize_string(cls, value: str, max_length: int = 1000) -> str:
        """
        Sanitize string input to prevent injection attacks.

        Args:
            value: Input string to sanitize
            max_length: Maximum allowed length

        Returns:
            Sanitized string

        Raises:
            ValueError: If input is invalid
        """
        if not isinstance(value, str):
            raise ValueError("Input must be a string")

        # Remove null bytes and control characters
        sanitized = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", value)

        # HTML escape to prevent XSS
        sanitized = html.escape(sanitized.strip())

        # Limit length
        if len(sanitized) > max_length:
            raise ValueError(f"Input too long (max {max_length} characters)")

        return sanitized

    @classmethod
    def validate_email(cls, email: str) -> str:
        """
        Validate and normalize email address.

        Args:
            email: Email address to validate

        Returns:
            Normalized email address

        Raises:
            ValueError: If email is invalid
        """
        try:
            # Use email-validator library for robust validation
            valid = validate_email(email)
            return valid.email.lower()
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email address: {str(e)}")

    @classmethod
    def validate_phone(cls, phone: str) -> str:
        """
        Validate phone number format.

        Args:
            phone: Phone number to validate

        Returns:
            Cleaned phone number

        Raises:
            ValueError: If phone format is invalid
        """
        if not phone:
            return ""

        cleaned = cls.sanitize_string(phone, 30)
        if not cls.PHONE_REGEX.match(cleaned):
            raise ValueError("Invalid phone number format")

        return cleaned

    @classmethod
    def validate_id(cls, client_id: str) -> str:
        """
        Validate ID format (alphanumeric, hyphens, underscores only).

        Args:
            client_id: ID to validate

        Returns:
            Validated ID

        Raises:
            ValueError: If ID format is invalid
        """
        if not client_id or not isinstance(client_id, str):
            raise ValueError("ID cannot be empty")

        cleaned = client_id.strip()
        if not cls.CLIENT_ID_REGEX.match(cleaned):
            raise ValueError("ID contains invalid characters")

        return cleaned

    @classmethod
    def validate_name(cls, name: str) -> str:
        """
        Validate person or company name.

        Args:
            name: Name to validate

        Returns:
            Validated name

        Raises:
            ValueError: If name is invalid
        """
        if not name or not isinstance(name, str):
            raise ValueError("Name cannot be empty")

        cleaned = cls.sanitize_string(name, 200)
        if not cls.NAME_REGEX.match(cleaned):
            raise ValueError("Name contains invalid characters")

        return cleaned

    @classmethod
    def validate_amount(cls, amount: Union[str, int, float, Decimal]) -> float:
        """
        Validate monetary amount.

        Args:
            amount: Amount to validate

        Returns:
            Validated amount as float

        Raises:
            ValueError: If amount is invalid
        """
        try:
            if isinstance(amount, str):
                # Remove common currency symbols and whitespace
                cleaned = re.sub(r"[$€£¥\s,]", "", amount)
                amount_decimal = Decimal(cleaned)
            else:
                amount_decimal = Decimal(str(amount))

            if amount_decimal < 0:
                raise ValueError("Amount cannot be negative")

            if amount_decimal > Decimal("999999999.99"):
                raise ValueError("Amount too large")

            return float(amount_decimal)

        except (InvalidOperation, TypeError):
            raise ValueError("Invalid amount format")

    @classmethod
    def validate_json_safe(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that data is JSON-safe and doesn't contain malicious content.

        Args:
            data: Dictionary to validate

        Returns:
            Validated dictionary

        Raises:
            ValueError: If data contains unsafe content
        """
        try:
            # Test JSON serialization
            json_str = json.dumps(data)
            if len(json_str) > 100000:  # 100KB limit
                raise ValueError("Data payload too large")

            # Check for potential script injection
            dangerous_patterns = [
                r"<script[^>]*>",
                r"javascript:",
                r"on\w+\s*=",
                r"eval\s*\(",
                r"function\s*\(",
            ]

            for pattern in dangerous_patterns:
                if re.search(pattern, json_str, re.IGNORECASE):
                    raise ValueError("Data contains potentially malicious content")

            return data

        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid data format: {str(e)}")

    @classmethod
    def validate_client_data(
        cls, data: Dict[str, Any], is_update: bool = False
    ) -> Dict[str, Any]:
        """
        Validate client data using Pydantic models.

        Args:
            data: Client data to validate
            is_update: Whether this is an update operation

        Returns:
            Validated client data

        Raises:
            ValueError: If validation fails
        """
        try:
            if is_update:
                client_model = ClientUpdate(**data)
            else:
                client_model = ClientCreate(**data)

            return client_model.dict(exclude_unset=True)

        except PydanticValidationError as e:
            errors = []
            for error in e.errors():
                field = ".".join(str(loc) for loc in error["loc"])
                errors.append(f"{field}: {error['msg']}")
            raise ValueError(f"Validation errors: {'; '.join(errors)}")

    @classmethod
    def validate_search_params(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate search parameters.

        Args:
            params: Search parameters to validate

        Returns:
            Validated search parameters

        Raises:
            ValueError: If validation fails
        """
        validated = {}

        # Validate query string
        if "query" in params and params["query"]:
            validated["query"] = cls.sanitize_string(params["query"], 200)

        # Validate balance filters
        if "min_balance" in params and params["min_balance"] is not None:
            validated["min_balance"] = cls.validate_amount(params["min_balance"])

        if "max_balance" in params and params["max_balance"] is not None:
            validated["max_balance"] = cls.validate_amount(params["max_balance"])

        # Validate balance range
        if (
            "min_balance" in validated
            and "max_balance" in validated
            and validated["min_balance"] > validated["max_balance"]
        ):
            raise ValueError("Minimum balance cannot be greater than maximum balance")

        return validated

    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """
        Sanitize filename to prevent path traversal attacks.

        Args:
            filename: Filename to sanitize

        Returns:
            Sanitized filename

        Raises:
            ValueError: If filename is invalid
        """
        if not filename or not isinstance(filename, str):
            raise ValueError("Filename cannot be empty")

        # Remove directory separators and dangerous characters
        sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "", filename)
        sanitized = sanitized.replace("..", "").strip()

        if not sanitized or sanitized in [".", ".."]:
            raise ValueError("Invalid filename")

        if len(sanitized) > 255:
            raise ValueError("Filename too long")

        return sanitized

    @classmethod
    def validate_date_string(cls, date_str: str) -> datetime:
        """
        Validate and parse date string.

        Args:
            date_str: Date string to validate

        Returns:
            Parsed datetime object

        Raises:
            ValueError: If date format is invalid
        """
        if not date_str:
            raise ValueError("Date cannot be empty")

        # Try common date formats
        date_formats = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%m/%d/%Y",
            "%d/%m/%Y",
        ]

        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        raise ValueError(f"Invalid date format: {date_str}")


# Convenience functions for common validations
def safe_string(value: Any, max_length: int = 1000) -> str:
    """Safely convert and validate string input."""
    if value is None:
        return ""
    return InputValidator.sanitize_string(str(value), max_length)


def safe_email(value: str) -> str:
    """Safely validate email address."""
    return InputValidator.validate_email(value)


def safe_amount(value: Any) -> float:
    """Safely validate monetary amount."""
    return InputValidator.validate_amount(value)


def safe_id(value: str) -> str:
    """Safely validate ID format."""
    return InputValidator.validate_id(value)
