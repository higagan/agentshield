"""Tests for the AgentShield PolicyEngine."""

from agentshield.engine import PolicyEngine, PolicyResult
from agentshield.rules import Violation


class TestPolicyEngine:
    """Tests for the PolicyEngine class."""

    def test_runs_policies_in_order(self):
        """Ensure it runs policies in the order they are provided."""
        execution_order = []

        def policy_one(data: object) -> Violation | None:
            execution_order.append("policy_one")
            return None

        def policy_two(data: object) -> Violation | None:
            execution_order.append("policy_two")
            return None

        engine = PolicyEngine(policies=[policy_one, policy_two])
        engine.run("test")

        assert execution_order == ["policy_one", "policy_two"]

    def test_short_circuits_on_first_violation(self):
        """Ensure it short-circuits on the first violation."""
        execution_order = []

        def policy_one(data: object) -> Violation | None:
            execution_order.append("policy_one")
            return Violation(rule_name="PolicyOne", reason="Blocked by policy one")

        def policy_two(data: object) -> Violation | None:
            execution_order.append("policy_two")
            return None

        engine = PolicyEngine(policies=[policy_one, policy_two])
        result = engine.run("test")

        assert isinstance(result, PolicyResult)
        assert result.allowed is False
        assert result.reason == "Blocked by policy one"
        assert execution_order == ["policy_one"]  # policy_two should not run

    def test_returns_allowed_if_all_pass(self):
        """Ensure it returns an allowed result if all policies pass."""

        def policy_one(data: object) -> Violation | None:
            return None

        def policy_two(data: object) -> Violation | None:
            return None

        engine = PolicyEngine(policies=[policy_one, policy_two])
        result = engine.run("test")

        assert isinstance(result, PolicyResult)
        assert result.allowed is True
        assert result.reason is None
