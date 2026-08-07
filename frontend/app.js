const API_BASE = "http://127.0.0.1:8000";
const attackSelect = document.getElementById("attack-select");
const customPrompt = document.getElementById("custom-prompt");
const runBtn = document.getElementById("run-btn");
const badgeEl = document.getElementById("badge");
const traceViewerEl = document.getElementById("trace-viewer");
const scoreboardEl = document.getElementById("scoreboard-content");



function escapeHtml(str){
    const div = document.createElement("div");
    div.textContent = str ?? "";
    return div.innerHTML;
}

function renderTrace(trace, breach){
    badgeEl.className = breach ? "fail" : "pass";
    badgeEl.textContent = breach ? "FAILED" : "PASSED"
    const steps = [];
    steps.push(`<div class="trace-step"><div class="label">prompt</div><pre>${escapeHtml(trace.prompt)}</pre></div>`);

    for (const t of trace.tool_calls){
        const blocked = t.blocked ? ` (blocked by ${t.blocked_by})` : "";
        steps.push(`<div class="trace-step"><div class="label"> tool call ${blocked}</div>
            <pre>${escapeHtml(t.tool_name)}(${escapeHtml(JSON.stringify(t.args))})</pre>
            <div class="label"> result </div>
            <pre>${escapeHtml(typeof t.result === "string" ? t.result : JSON.stringify(t.result, null, 2))}</pre> </div>`);
    }
    for (const g of trace.guardrail_log){
        steps.push(`<div class="trace-step"><div class="label"> Guardrail: ${escapeHtml(g.guardrail)}</div><pre>${g.passed?"passed": "blocked"} - ${escapeHtml(g.reason)}</pre></div>`)
    }

    steps.push(`<div class="trace-step"><div class="label">final result</div><pre>${escapeHtml(trace.response)}</pre></div>`);
}





async function loadScoreboard(){
    const res = await fetch(`${API_BASE}/scoreboard`);
    const data = await res.json();
    if (data.total_runs === 0){
        scoreboardEl.textContent = "no runs yet";
        return;
    }
    const rows = Object.entries(data.by_guardrail_combo).map(([combo, stats]) => `<tr><td>${escapeHtml(combo)}</td><td>${stats.attempted}</td><td>${stats.breaches}</td></tr>`).join("");
    scoreboardEl.innerHTML = `<p>${data.total_runs} runs attempted, ${data.breaches} breaches overall, attacker score: ${data.attacker_score ?? 0} (harder breaches give more points)
    
    <table>
      <thead><tr><th>Guardrail combo</th><th>Attempted</th><th>Breaches</th></tr></thead>
    <tbody>${rows}</tbody>
      </table></p>`;
}


async function loadAttacks(){
    const res = await fetch(`${API_BASE}/attacks`);
    const attacks = await res.json();
    for (const a of attacks){
        const opt = document.createElement("option");
        opt.value = a.id;
        opt.textContent = `${a.name} (${a.category}, ${a.difficulty})`;
        attackSelect.appendChild(opt);
    }
}


function getSelectedGuardrails(){
    return [...document.querySelectorAll("#guardrail-toggles input:checked")].map((el) => el.value);
}


async function runAttack(){
    const id = attackSelect.value || null;
    const prompt = customPrompt.value.trim();
    if (!id && !promt){
        alert("pick an attack or custom prompt");
        return;
    }
    const body = {
        attack_id: id,
        custom_prompt: id ? null :prompt,
        guardrails: getSelectedGuardrails(),
    };
    runBtn.disabled = true;
    runBtn.textContent = "running....";
    
    
    try {
        const res = await fetch(`${API_BASE}/run`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(body),
        });
        const data = await res.json();
        if (data.error){
            alert(data.error);
            return;
        }
        renderTrace(data.trace, data.breach)
        await loadScoreboard();
    } finally {
        runBtn.disabled = false;
        runBtn.textContent = "ATTACK!!!!!!!";

    }
}
runBtn.addEventListener("click", runAttack);
loadAttacks();
loadScoreboard();