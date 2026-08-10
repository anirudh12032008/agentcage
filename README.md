# battel

this is a tool using llm agents gets attacked with a library of prompt injection payloads you can toggle three different guadrails on and off and a scoreboard tracks what got through and what didn't


## whats actually happening?
- a fastapi backend runs a agent loop 
- the agent has 3 tools: read_file, web_fetch, send_email ( the most fun one lol )
- 12 different attack payloads in YAML files which are split into direct injections, indirect injections and tool-hijack 
