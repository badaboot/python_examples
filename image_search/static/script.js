const API = "http://localhost:8000";

document.getElementById("query").addEventListener("keydown", (e) => {
    if (e.key === "Enter") runSearch();
});

async function runSearch() {
    const query = document.getElementById("query").value.trim();
    const top_k = parseInt(document.getElementById("topk").value);
    const btn = document.getElementById("searchBtn");
    const status = document.getElementById("status");
    const results = document.getElementById("results");

    if (!query) {
        setStatus("Please enter a query.", "error");
        return;
    }

    btn.disabled = true;
    results.innerHTML = "";
    setStatus("Searching...");

    try {
        const res = await fetch(`${API}/search`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, top_k }), // folder_path removed
        });

        const data = await res.json();

        if (!res.ok) {
            setStatus(data.detail || "Server error.", "error");
            return;
        }

        setStatus("");
        renderResults(data.query, data.results);
    } catch (err) {
        setStatus("Could not reach server. Is FastAPI running?", "error");
    } finally {
        btn.disabled = false;
    }
}

function renderResults(query, results) {
    const container = document.getElementById("results");
    container.innerHTML = `<div class="query-tag">Results for: <span>${query}</span></div>`;

    const maxScore = Math.max(...results.map((r) => r.score));

    results.forEach((r) => {
        const pct = ((r.score / maxScore) * 100).toFixed(1);
        const card = document.createElement("div");
        card.className = "result-card";
        card.innerHTML = `
      <div class="rank">#${r.rank}</div>
      <img 
        src="http://localhost:8000/images/${encodeURIComponent(r.filename)}" 
        alt="${r.filename}"
        style="width:80px; height:80px; object-fit:cover; border-radius:6px; flex-shrink:0;"
        onerror="this.style.display='none'"
      />
      <div class="file-info">
        <div class="filename">${r.filename}</div>
        <div class="filepath">${r.filepath}</div>
      </div>
      <div class="score-bar-wrap">
        <div class="score-label">${r.score}</div>
        <div class="score-bar-bg">
          <div class="score-bar-fill" style="width: ${pct}%"></div>
        </div>
      </div>
    `;
        container.appendChild(card);
    });
}

function setStatus(msg, type = "") {
    const el = document.getElementById("status");
    el.textContent = msg;
    el.className = "status " + type;
}