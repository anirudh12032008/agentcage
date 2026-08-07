NAME = 'output_redaction'
_SECRET = "sk-this-is-a-fake-secret"

def check(t:str) -> tuple[bool, str]:
    if _SECRET in t:
        return False, "contains secret"
    return True, "no secret"