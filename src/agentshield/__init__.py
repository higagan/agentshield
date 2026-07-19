"""AgentShield: a lightweight shield for intercepting agent tool calls."""

from agentshield.decorator import shield_tool
from agentshield.engine import PolicyEngine, PolicyResult
from agentshield.exceptions import AgentShieldBlockError
from agentshield.rules import SensitiveDataFilter, URLAllowList, Violation

__all__ = [
    "shield_tool",
    "AgentShieldBlockError",
    "SensitiveDataFilter",
    "URLAllowList",
    "Violation",
    "PolicyEngine",
    "PolicyResult",
]
__version__ = "0.1.0"
