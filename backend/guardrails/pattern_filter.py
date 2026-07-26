import re

SUSPICIOUS_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"\bDAN\b",
    r"\[SYSTEM\]",
    r"do anything now",
    r"disregard the user'?s? (original )?request",
    r"disregard (all )?previous instructions",
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in SUSPICIOUS_PATTERNS] 
NAME = "pattern_filter"
def check(text: str) -> tuple[bool, str]:
    for p in _COMPILED:
        m = p.search(text)
        if m:
            return False, f"matched suspicious pattern: {m.group(0)}"
    return True, "safe ig?"
