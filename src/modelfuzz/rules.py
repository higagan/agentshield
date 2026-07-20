"""Security rules for ModelFuzz."""

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class Violation:
    """Represents a policy violation."""

    rule_name: str
    reason: str


class URLAllowList:
    """A policy that ensures URLs are on an allowlist and blocks parsing tricks."""

    def __init__(self, allowed_domains: list[str]) -> None:
        self.allowed_domains = allowed_domains

    def __call__(self, url: str) -> Violation | None:
        """Check if a URL is allowed.

        Args:
            url: The URL to check.

        Returns:
            A Violation object if the URL is blocked, otherwise None.
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc

            # Block userinfo tricks (e.g., http://api.internal.com@evil.com)
            if "@" in domain:
                return Violation(
                    rule_name="URLAllowList",
                    reason=f"URL contains userinfo trick: {url}",
                )

            # Extract the hostname without port
            hostname = domain.split(":")[0]

            # Check for exact match or valid subdomain
            is_allowed = any(
                hostname == allowed or hostname.endswith(f".{allowed}")
                for allowed in self.allowed_domains
            )

            if not is_allowed:
                return Violation(
                    rule_name="URLAllowList",
                    reason=f"URL domain not in allowlist: {hostname}",
                )

            return None

        except Exception:
            return Violation(
                rule_name="URLAllowList",
                reason=f"Invalid URL: {url}",
            )


class SensitiveDataFilter:
    """A policy that blocks strings containing sensitive keywords."""

    def __init__(self, sensitive_keywords: list[str] | None = None) -> None:
        self.sensitive_keywords = (
            [k.lower() for k in sensitive_keywords]
            if sensitive_keywords
            else ["secret", "password", "api_key"]
        )

    def __call__(self, data: object) -> Violation | None:
        """Check if data contains sensitive keywords.

        This method recurses into nested dicts, lists, and tuples.

        Args:
            data: The data to check.

        Returns:
            A Violation object if sensitive data is found, otherwise None.
        """
        return self._check_recursive(data)

    def _check_recursive(self, data: object) -> Violation | None:
        if isinstance(data, str):
            lower_data = data.lower()
            for keyword in self.sensitive_keywords:
                if keyword in lower_data:
                    return Violation(
                        rule_name="SensitiveDataFilter",
                        reason=f"String contains sensitive keyword: '{keyword}'",
                    )
        elif isinstance(data, dict):
            for value in data.values():
                violation = self._check_recursive(value)
                if violation:
                    return violation
        elif isinstance(data, (list, tuple)):
            for item in data:
                violation = self._check_recursive(item)
                if violation:
                    return violation

        return None
