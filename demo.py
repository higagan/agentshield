"""Demo script showing AgentShield's `shield_tool` decorator in action."""

from agentshield import shield_tool


@shield_tool()
def fetch_weather(city: str) -> str:
    """Pretend tool that fetches the weather for a city."""
    return f"The weather in {city} is sunny."


@shield_tool()
def calculate_sum(a: int, b: int) -> int:
    """Pretend tool that adds two numbers."""
    return a + b


@shield_tool()
def send_email(to: str, subject: str, body: str) -> str:
    """Pretend tool that sends an email."""
    return f"Email sent to {to} with subject '{subject}'."


def main() -> None:
    print("=== AgentShield Demo ===\n")

    print("Calling fetch_weather('London'):")
    print(fetch_weather("London"))

    print("\nCalling calculate_sum(3, 4):")
    print(calculate_sum(3, 4))

    print("\nCalling send_email('alice@example.com', 'Hello', 'Hi Alice!'):")
    print(send_email("alice@example.com", "Hello", "Hi Alice!"))


if __name__ == "__main__":
    main()
