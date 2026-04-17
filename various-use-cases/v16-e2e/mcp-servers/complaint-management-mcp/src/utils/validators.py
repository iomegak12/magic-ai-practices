"""
Validators Module

Provides input validation functions for complaint management fields.
All validators raise ValueError with a descriptive message on failure.
"""

import re

# Regex patterns
_TITLE_PATTERN = re.compile(r"^[\w\s\-_,\.]+$")
_CUSTOMER_NAME_PATTERN = re.compile(r"^[A-Za-z\s]+$")
_ORDER_NUMBER_PATTERN = re.compile(r"^ORD-\d{5,}$")

# Field length constraints
TITLE_MIN_LEN = 5
TITLE_MAX_LEN = 200
DESCRIPTION_MIN_LEN = 10
DESCRIPTION_MAX_LEN = 2000
CUSTOMER_NAME_MIN_LEN = 2
CUSTOMER_NAME_MAX_LEN = 100


def validate_title(value: str) -> str:
    """
    Validate a complaint title.

    Rules:
    - Length: 5–200 characters
    - Allowed characters: alphanumeric, spaces, hyphens, underscores, commas, periods

    Args:
        value: The title string to validate.

    Returns:
        The stripped, validated title.

    Raises:
        ValueError: If validation fails.
    """
    if not isinstance(value, str):
        raise ValueError("Title must be a string.")

    value = value.strip()

    if len(value) < TITLE_MIN_LEN:
        raise ValueError(
            f"Title must be at least {TITLE_MIN_LEN} characters long. "
            f"Got {len(value)}."
        )

    if len(value) > TITLE_MAX_LEN:
        raise ValueError(
            f"Title must not exceed {TITLE_MAX_LEN} characters. "
            f"Got {len(value)}."
        )

    if not _TITLE_PATTERN.match(value):
        raise ValueError(
            "Title contains invalid characters. "
            "Allowed: alphanumeric, spaces, hyphens (-), underscores (_), "
            "commas (,), and periods (.)."
        )

    return value


def validate_description(value: str) -> str:
    """
    Validate a complaint description.

    Rules:
    - Length: 10–2000 characters
    - No character restrictions (free-form text)

    Args:
        value: The description string to validate.

    Returns:
        The stripped, validated description.

    Raises:
        ValueError: If validation fails.
    """
    if not isinstance(value, str):
        raise ValueError("Description must be a string.")

    value = value.strip()

    if len(value) < DESCRIPTION_MIN_LEN:
        raise ValueError(
            f"Description must be at least {DESCRIPTION_MIN_LEN} characters long. "
            f"Got {len(value)}."
        )

    if len(value) > DESCRIPTION_MAX_LEN:
        raise ValueError(
            f"Description must not exceed {DESCRIPTION_MAX_LEN} characters. "
            f"Got {len(value)}."
        )

    return value


def validate_customer_name(value: str) -> str:
    """
    Validate a customer name.

    Rules:
    - Length: 2–100 characters
    - Allowed characters: letters (A-Z, a-z) and spaces only

    Args:
        value: The customer name string to validate.

    Returns:
        The stripped, validated customer name.

    Raises:
        ValueError: If validation fails.
    """
    if not isinstance(value, str):
        raise ValueError("Customer name must be a string.")

    value = value.strip()

    if len(value) < CUSTOMER_NAME_MIN_LEN:
        raise ValueError(
            f"Customer name must be at least {CUSTOMER_NAME_MIN_LEN} characters long. "
            f"Got {len(value)}."
        )

    if len(value) > CUSTOMER_NAME_MAX_LEN:
        raise ValueError(
            f"Customer name must not exceed {CUSTOMER_NAME_MAX_LEN} characters. "
            f"Got {len(value)}."
        )

    if not _CUSTOMER_NAME_PATTERN.match(value):
        raise ValueError(
            "Customer name contains invalid characters. "
            "Only letters (A–Z, a–z) and spaces are allowed."
        )

    return value


def validate_order_number(value: str) -> str:
    """
    Validate an order number.

    Rules:
    - Format: ORD-NNNNN (prefix 'ORD-' followed by at least 5 digits)
    - Examples: ORD-10001, ORD-99999, ORD-100000

    Args:
        value: The order number string to validate.

    Returns:
        The stripped, validated order number.

    Raises:
        ValueError: If validation fails.
    """
    if not isinstance(value, str):
        raise ValueError("Order number must be a string.")

    value = value.strip()

    if not _ORDER_NUMBER_PATTERN.match(value):
        raise ValueError(
            f"Order number '{value}' is invalid. "
            "Expected format: ORD-NNNNN (e.g. ORD-10001). "
            "Must start with 'ORD-' followed by at least 5 digits."
        )

    return value
