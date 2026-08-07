import json
import uuid
from pathlib import Path

PATH = Path(__file__).parent / "trace_store.json"
MAX_STORED = 50

def _load()-> list[dict]:
    if PATH.exists():
        return json.loads(PATH.read_text())
    return []

def _save(hist: list[dict]):
    PATH.write_text(json.dumps(hist, indent=2))

def save_trace(trace: dict) -> str:
    hist = _load()
    id = uuid.uuid4().hex[:12]
    hist.append({"id": id, "trace": trace})
    hist = hist[-MAX_STORED:]
    _save(hist)
    return id



def get_trace(id: str) -> dict | None:
    for entry in _load():
        if entry["id"] == id:
            return entry["trace"]
    return None