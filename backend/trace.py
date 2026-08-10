from dataclasses import dataclass, field
from typing import Any

@dataclass
class ToolCallRecord:
    tool_name: str
    args: dict[str, Any]
    result: Any
    blocked_by: str | None = None



@dataclass
class Trace:
    user_prompt: str
    attack_name: str | None = None
    guardrails: list[str] = field(default_factory=list)
    tool_calls: list[ToolCallRecord] = field(default_factory=list)
    response: str | None = None
    guardrail_log: list[dict[str, Any]] = field(default_factory=list)

    def log_guardrail(self, name: str, passed: bool, reason: str):
        self.guardrail_log.append({"guardrail": name, "passed": passed, "reason": reason})

    def to_dict(self) -> dict:
        return {
            "user_prompt": self.user_prompt,
            "attack_name": self.attack_name,
            "guardrails": self.guardrails,
            "tool_calls": [ {
                "tool_name": tc.tool_name,
                "args": tc.args,
                "result": tc.result,
                "blocked_by": tc.blocked_by,
            } for tc in self.tool_calls ],
            "response": self.response,
            "guardrail_log": self.guardrail_log,
        }