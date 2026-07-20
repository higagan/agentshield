"""ModelFuzz: a lightweight shield for intercepting agent tool calls."""

from modelfuzz.decorator import shield_tool
from modelfuzz.engine import PolicyEngine, PolicyResult
from modelfuzz.exceptions import ModelFuzzBlockError
from modelfuzz.rules import SensitiveDataFilter, URLAllowList, Violation

__all__ = [
    "shield_tool",
    "ModelFuzzBlockError",
    "SensitiveDataFilter",
    "URLAllowList",
    "Violation",
    "PolicyEngine",
    "PolicyResult",
]
__version__ = "0.1.0"
