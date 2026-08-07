import itertools
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))




from agent import run_agent
from trace import Trace
from attacks.loader import load_attacks
from scoreboard import breached 

ALL_G = ["pattern_filter", "sandbox_delimiter", "judge_llm", "output_redaction"]

COMBOS = [
    set(c)
    for i in range(len(ALL_G)+1)
    for c in itertools.combinations(ALL_G, i)
]


attacks = load_attacks()
print(f"{len(attacks)} attacks  {len(COMBOS)} guardrail combos = {len(attacks)*len(COMBOS)} runs\n")


for a in attacks:
    row = [
    ]
    for g in COMBOS:
        trace = Trace(user_prompt=a["payload"], attack_name=a["name"])
        run_agent(a["payload"], trace, guardrails=g)
        row.append("X" if breached(trace) else ".")
    print(f"{a['id']:40} {''.join(row)}")

print("\n combos (left o right, matches column order above):")
for i, c in enumerate(COMBOS):
    print(f"{i:2}: {','.join(sorted(c)) or 'none'}")