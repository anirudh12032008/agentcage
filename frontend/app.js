const API_BASE = "http://127.0.0.1:8000";
const attackSelect = document.getElementById("attack-select");
const customPrompt = document.getElementById("custom-prompt");
const runBtn = document.getElementById("run-btn");

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
        console.log("result", data);
    } finally {
        runBtn.disabled = false;
        runBtn.textContent = "ATTACK!!!!!!!";

    }
}
runBtn.addEventListener("click", runAttack);
loadAttacks();