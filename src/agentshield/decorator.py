"""Decorators for shielding agent tool functions."""

import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def shield_tool(func: Callable[P, R]) -> Callable[P, R]:
    """Wrap a tool function so every call is intercepted before execution.

    Announces the interception by printing the wrapped function's name,
    then executes the function with its original arguments.

    Args:
        func: The tool function to shield.

    Returns:
        The wrapped function, preserving the original signature and metadata.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"AgentShield Intercepted: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper
