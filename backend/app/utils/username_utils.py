"""
Username transformation utilities for Cognito compatibility.
Cognito has issues with @ symbols in usernames, so we transform emails.
"""
import re
from typing import Optional


def email_to_cognito_username(email: str) -> str:
    """
    Transform email to Cognito-compatible username.
    Replace @ with _ for Cognito compatibility.
    
    Example: iliagerman@gmail.com -> iliagerman_gmail.com
    """
    if not email or "@" not in email:
        return email
    
    # Replace @ with _
    return email.replace("@", "_")


def cognito_username_to_email(username: str) -> str:
    """
    Transform Cognito username back to email format.
    Replace the last _ with @ to restore email format.
    
    Example: iliagerman_gmail.com -> iliagerman@gmail.com
    """
    if not username or "_" not in username:
        return username
    
    # Find the last underscore and replace it with @
    # This handles cases where there might be underscores in the local part
    last_underscore_index = username.rfind("_")
    if last_underscore_index == -1:
        return username
    
    # Check if the part after the last underscore looks like a domain
    domain_part = username[last_underscore_index + 1:]
    if "." in domain_part:
        # Replace the last underscore with @
        return username[:last_underscore_index] + "@" + domain_part
    
    return username


def is_valid_email(email: str) -> bool:
    """
    Validate email format.
    """
    if not email:
        return False
    
    # Basic email validation regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None


def normalize_email(email: str) -> str:
    """
    Normalize email address (lowercase, strip whitespace).
    """
    if not email:
        return email
    
    return email.strip().lower()


def validate_and_transform_email(email: str) -> tuple[str, str]:
    """
    Validate email and return both normalized email and Cognito username.
    
    Returns:
        tuple: (normalized_email, cognito_username)
    
    Raises:
        ValueError: If email is invalid
    """
    if not email:
        raise ValueError("Email is required")
    
    # Normalize email
    normalized_email = normalize_email(email)
    
    # Validate email format
    if not is_valid_email(normalized_email):
        raise ValueError("Invalid email format")
    
    # Transform to Cognito username
    cognito_username = email_to_cognito_username(normalized_email)
    
    return normalized_email, cognito_username


# Example usage and tests
if __name__ == "__main__":
    # Test cases
    test_emails = [
        "iliagerman@gmail.com",
        "user.name@example.org",
        "test+tag@domain.co.uk",
        "simple@test.com"
    ]
    
    print("Testing email to username transformation:")
    for email in test_emails:
        try:
            normalized, username = validate_and_transform_email(email)
            restored = cognito_username_to_email(username)
            print(f"Original: {email}")
            print(f"Normalized: {normalized}")
            print(f"Cognito Username: {username}")
            print(f"Restored: {restored}")
            print(f"Match: {normalized == restored}")
            print("-" * 40)
        except ValueError as e:
            print(f"Error with {email}: {e}")
            print("-" * 40)
