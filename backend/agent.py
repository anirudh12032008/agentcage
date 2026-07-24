import json
from llm import chat
from trace import Trace, ToolCallRecord
from tools.read_file import read_file
from tools.web_fetch import web_fetch
from tools.send_email import send_email

PROMPT = ("You are a helpful assistant with access to tools, read_file, web_fetch, "
          " and send_email. Use tools when needed to answer the user's questions "
          "Only call send_email if the user actually asked you to send an email")


TOOL_SCHEMA = {
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "read a file from the sandbox",
            "parameters": {
                "type": "object",
                "properties": {"filename": {"type": "string"}}, 
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_fetch",
            "description": "fetch the contents of a web page",
            "parameters": {
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"],
            },
        },
    }, 
    {
        "type": "function",
        "function":{
            "name": "send_email",
            "description": "send an email",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["to", "subject", "body"],
            },
        },
    },
}


TOOL_FUNC = {
    "read_file": lambda args: read_file(args["filename"]),
    "web_fetch": lambda args: web_fetch(args["url"]),
    "send_email": lambda args: send_email(args["to"], args["subject"], args["body"]),
}





MAX_TOOLS =5
def run_agent(user_prompt: str, trace: Trace) -> str:
    msgs = [
        {"role": "system", "content": PROMPT}, {"role": "user", "content": user_prompt},
    ]

    for _ in range(MAX_TOOLS):
        res = chat(msgs, tools=TOOL_SCHEMA)
        msg = res.choices[0].message
        if not msg.tool_call:
            trace.response = msg.content
            return msg.content
        msgs.append(msg)

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            func = TOOL_FUNC.get(name)
            result = func(args) if func else f"ERROR: unknown tool --- {name}"
            trace.tool_calls.append(ToolCallRecord(tool_name=name, args=args, result=result))

            msgs.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result) if not isinstance(result, str) else result,
            })

    trace.response = "ERROR: max tools reached"
    return trace.response