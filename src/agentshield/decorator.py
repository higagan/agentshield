"""Decorators for shielding agent tool functions."""

import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar

from agentshield.engine import PolicyEngine
from agentshield.exceptions import AgentShieldBlockError
from agentshield.rules import SensitiveDataFilter

P = ParamSpec("P")
R = TypeVar("R")

# Default policy engine for the decorator
default_policies = [SensitiveDataFilter()]
_default_engine = PolicyEngine(default_policies)


def shield_tool(engine: PolicyEngine | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Wrap a tool function so every call is intercepted before execution.

    Args:
        engine: The policy engine to use for validation. If None, a default
            engine with a SensitiveDataFilter is used.

    Returns:
        A decorator that wraps the function.
    """
    actual_engine = engine if engine is not None else _default_engine

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Check all arguments against the policy engine
            for arg in list(args) + list(kwargs.values()):
                result = actual_engine.run(arg)
                if not result.allowed:
                    raise AgentShieldBlockError(result.reason or "Call blocked by policy")

            print(f"AgentShield Intercepted: {func.__name__}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
