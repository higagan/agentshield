"""Tests for AgentShield security rules."""

import pytest

from agentshield.rules import SensitiveDataFilter, URLAllowList


class TestURLAllowList:
    """Tests for the URLAllowList policy."""

    @pytest.fixture
    def url_allowlist(self) -> URLAllowList:
        """Fixture for a URLAllowList with 'api.internal.com' allowed."""
        return URLAllowList(allowed_domains=["api.internal.com"])

    def test_blocks_evil_domain(self, url_allowlist: URLAllowList):
        """Ensure it blocks http://evil.com."""
        violation = url_allowlist("http://evil.com")
        assert violation is not None
        assert "not in allowlist" in violation.reason

    def test_allows_internal_domain(self, url_allowlist: URLAllowList):
        """Ensure it allows http://api.internal.com."""
        violation = url_allowlist("http://api.internal.com")
        assert violation is None

    def test_blocks_subdomain_trick(self, url_allowlist: URLAllowList):
        """Ensure it blocks http://api.internal.com.evil.com."""
        violation = url_allowlist("http://api.internal.com.evil.com")
        assert violation is not None
        assert "not in allowlist" in violation.reason

    def test_blocks_path_trick(self, url_allowlist: URLAllowList):
        """Ensure it blocks http://evil.com/api.internal.com."""
        violation = url_allowlist("http://evil.com/api.internal.com")
        assert violation is not None
        assert "not in allowlist" in violation.reason

    def test_blocks_userinfo_trick(self, url_allowlist: URLAllowList):
        """Ensure it blocks http://api.internal.com@evil.com."""
        violation = url_allowlist("http://api.internal.com@evil.com")
        assert violation is not None
        assert "userinfo trick" in violation.reason


class TestSensitiveDataFilter:
    """Tests for the SensitiveDataFilter policy."""

    @pytest.fixture
    def filter(self) -> SensitiveDataFilter:
        """Fixture for a SensitiveDataFilter with default keywords."""
        return SensitiveDataFilter()

    def test_blocks_secret_string(self, filter: SensitiveDataFilter):
        """Ensure it blocks strings containing 'secret'."""
        violation = filter("This is a secret message")
        assert violation is not None
        assert "secret" in violation.reason

    def test_blocks_password_string_case_insensitive(self, filter: SensitiveDataFilter):
        """Ensure it blocks strings containing 'PASSWORD' (case-insensitive)."""
        violation = filter("My PASSWORD is 12345")
        assert violation is not None
        assert "password" in violation.reason

    def test_blocks_api_key_string(self, filter: SensitiveDataFilter):
        """Ensure it blocks strings containing 'api_key'."""
        violation = filter("The api_key is abc")
        assert violation is not None
        assert "api_key" in violation.reason

    def test_recurses_into_nested_dicts(self, filter: SensitiveDataFilter):
        """Ensure it recurses into nested dicts."""
        data = {"level1": {"level2": {"level3": "contains password"}}}
        violation = filter(data)
        assert violation is not None

    def test_recurses_into_nested_lists(self, filter: SensitiveDataFilter):
        """Ensure it recurses into nested lists."""
        data = ["clean", ["clean", ["secret data"]]]
        violation = filter(data)
        assert violation is not None

    def test_recurses_into_nested_tuples(self, filter: SensitiveDataFilter):
        """Ensure it recurses into nested tuples."""
        data = ("clean", ("clean", ("api_key is here",)))
        violation = filter(data)
        assert violation is not None

    def test_allows_clean_data(self, filter: SensitiveDataFilter):
        """Ensure it allows clean data."""
        data = {"user": "alice", "action": "login"}
        violation = filter(data)
        assert violation is None
