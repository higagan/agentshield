"""Policy engine for AgentShield."""

from collections.abc import Callable
from dataclasses import dataclass

from agentshield.rules import Violation


@dataclass
class PolicyResult:
    """The result of a policy engine run."""

    allowed: bool
    reason: str | None = None


class PolicyEngine:
    """Runs a list of policies against a call."""

    def __init__(self, policies: list[Callable[[object], Violation | None]]) -> None:
        self.policies = policies

    def run(self, call: object) -> PolicyResult:
        """Run all policies in order. Short-circuit on first violation.

        Args:
            call: The call data to check.

        Returns:
            A PolicyResult object indicating if the call is allowed.
        """
        for policy in self.policies:
            violation = policy(call)
            if violation:
                return PolicyResult(allowed=False, reason=violation.reason)
        return PolicyResult(allowed=True)
