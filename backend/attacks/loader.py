from pathlib import Path
import yaml
DIR = Path(__file__).parent
REQ = { "name","category", "payload", "description", "difficulty"}

def load_attacks() -> list[dict]:
    attacks = []
    for f in sorted(DIR.glob("*.yaml")):
        with open(f) as fh:
            data = yaml.safe_load(f)
        missing = REQ - data.keys()
        if missing:
            raise ValueError(f"missing fields")
        data["id"] = f.stem
        attacks.append(data)
    return attacks

def get_attack(attack_id: str) -> dict | None:
    for attack in load_attacks():
        if attack["id"] == attack_id:
            return attack
    return None 
