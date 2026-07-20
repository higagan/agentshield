"""Tests for the ModelFuzz shield_tool decorator."""

import pytest

from modelfuzz import ModelFuzzBlockError, shield_tool


@shield_tool()
def send_email(to: str, subject: str, body: str) -> str:
    """Pretend tool that sends an email."""
    return f"Email sent to {to} with subject '{subject}'."


class TestShieldToolDecorator:
    """Tests for the shield_tool decorator."""

    def test_malicious_call_raises_block_error(self):
        """Assert that a malicious call raises ModelFuzzBlockError."""
        malicious_body = "My password is 12345"
        with pytest.raises(ModelFuzzBlockError):
            send_email("alice@example.com", "Hello", malicious_body)

    def test_safe_call_executes_successfully(self):
        """Assert that a safe call executes successfully and returns the correct output."""
        safe_body = "Hi Alice, how are you?"
        result = send_email("alice@example.com", "Hello", safe_body)
        assert result == "Email sent to alice@example.com with subject 'Hello'."

    def test_decorator_preserves_metadata(self):
        """Assert that the decorator preserves the function's metadata."""
        assert send_email.__name__ == "send_email"
        assert send_email.__doc__ == "Pretend tool that sends an email."
