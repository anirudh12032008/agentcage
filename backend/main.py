from fastAPI import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_agent
from attacks.loader import load_attack, get_attack
from scoreboard import record_run, breached, get_scoreboard
from trace import Trace
from security import check_api_key, check_rate_limit


app = FastAPI(title="battle")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/attacks")
def list_attacks():
    return load_attack

class RunRequest(BaseModel):
    attack_id: str | None = None
    custom_prompt: str | None = None
    guardrails: list[str] = []


@app.post("/run", dependencies=[Depends(check_api_key), Depends(check_rate_limit)])
def run(req: RunRequest):
    if req.attack_id:
        a = get_attack(req.attack_id)
        if not a:
            return {f"unknown attack": {req.attack_id}}
        prompt = a["payload"]
        name = a["name"]
    elif req.custom_prompt:
        prompt = req.custom_prompt
        name = None
    else:
        return {"error": "no id nor custom prompt given"}
    trace = Trace(user_prompt=prompt, attack_name=name)
    run_agent(prompt, trace, guardrails=set(req.guardrails))
    breach = breached(trace)
    record_run(trace, breach)
    return {"trace": trace.to_dict(), "breach": breach}






@app.get("/scoreboard")
def scoreboard():
    return get_scoreboard()