# battel

this is a tool using llm agents gets attacked with a library of prompt injection payloads you can toggle three different guadrails on and off and a scoreboard tracks what got through and what didn't


## whats actually happening?
- a fastapi backend runs a agent loop 
- the agent has 3 tools: read_file, web_fetch, send_email ( the most fun one lol )
- 12 different attack payloads in YAML files which are split into direct injections, indirect injections and tool-hijack 

## screenshots
<img width="1023" height="752" alt="Screenshot 2026-09-16 at 8 41 30 AM" src="https://github.com/user-attachments/assets/feec6869-907b-4a5b-a6d7-3a91707dc6f2" />
<img width="1435" height="1061" alt="Screenshot 2026-09-16 at 8 41 25 AM" src="https://github.com/user-attachments/assets/df94bf32-b590-4a4b-a02c-75c60f1daf47" />

### the guardrails
- pattern_filter: catches the obvious stuff
- sandbox_delimiter: makes untrusted content as a data not instruction
- output_redaction: removes secretts out of agent response
- judge_llm: check if agent got hijacked

## tech stack
- backend -> python, fastapi, pydantic, httpx
- llm -> groq llama-3.3-70b
- frontend -> html css js
- hosting -> render


## how i made it with the blockers
any llm available online doesn't want to get hacked its safetly training is good lol but that was sad for me
so i had to reqrite the system prompts a bunch of times so it knows its in a sandbox and not reallity( the commits are fun see them lol)

fake email were too sketchy so i had to change them too
and there were a few more blockers like breach detection was backwards, small models are flasky at json tool calls and frontend crashes
but somehow i did it :D
(m v v v proud of me lol)


## running it locally?
### what you need
- python, uv, groq api

### backend
    cd backend
    uv sync

make a `backend/.env`:

    GROQ_API_KEY=your_groq_key
    ARENA_API_KEY=any_secret_you_want

then:

    uv run uvicorn main:app --reload

### frontend
    API_BASE_URL=http://127.0.0.1:8000 node scripts/inject-env.js
### run every attack against every guardrail combo
    cd backend
    uv run python scripts/run_matrix.py


### ai disclosure
i designed the project and attacks and the guardrails myself, very less ai was used throughout the project dirctly
i used claude for debugging the scoreboard + frontend bugs and majorly for deployment config and in the ending when render sucks i had to take help onfg i hate render
