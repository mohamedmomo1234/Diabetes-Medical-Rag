import re


BLOCKED_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"show\s+(me\s+)?the\s+system\s+prompt",
    r"give\s+(me\s+)?the\s+system\s+prompt",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"show\s+(me\s+)?the\s+developer\s+prompt",
    r"reveal\s+(the\s+)?developer\s+prompt",
    r"show\s+(me\s+)?the\s+api\s*key",
    r"give\s+(me\s+)?the\s+api\s*key",
    r"reveal\s+(the\s+)?api\s*key",
    r"show\s+(me\s+)?the\s+password",
    r"give\s+(me\s+)?the\s+password",
    r"show\s+(me\s+)?environment\s+variables",
    r"show\s+(me\s+)?\.env",
    r"print\s+(the\s+)?environment\s+variables",
]


SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9_-]{10,}",
    r"gsk_[A-Za-z0-9_-]{10,}",
]


def security_check(question: str):
    text = question.lower().strip()

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text):
            return (
                False,
                "I can't provide system prompts, API keys, "
                "passwords, credentials, or private application data."
            )

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, text):
            return (
                False,
                "I can't process or reveal secret credentials."
            )

    return True, ""
