from pathlib import Path

DIR = (Path(__file__).parent.parent / "sandbox").resolve()

def read_file(filename: str) -> str:
    t = (DIR / filename).resolve()

    if DIR not in t.parents and t != DIR:
        return "ERROR: this is outside the sandbox"
    if not t.is_file():
        return "ERROR: no such file"
    return t.read_text()
