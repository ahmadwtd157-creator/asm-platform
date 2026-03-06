const API = "http://localhost:5000/api";
const token = localStorage.getItem("token");

function authHeader() {
    return { "Authorization": `Bearer ${token}` };
}

function riskBadge(score) {
    if (score < 30) return "badge bg-success";
    if (score < 70) return "badge bg-warning";
    return "badge bg-danger";
}

function getAssetId() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

async function loadResults() {
    const id = getAssetId();
    const res = await fetch(`${API}/assets/${id}/results`, {
        headers: authHeader()
    });

    const data = await res.json();
    const table = document.getElementById("resultsTable");
    table.innerHTML = "";

    data.forEach(r => {
        table.innerHTML += `
            <tr>
              <td>${r.port}</td>
              <td>${r.service}</td>
              <td>${r.banner}</td>
              <td>${r.is_open ? "Open" : "Closed"}</td>
              <td><span class="${riskBadge(r.risk_score)}">${r.risk_score}</span></td>
            </tr>
        `;
    });
}

loadResults();