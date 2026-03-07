const API = "http://localhost:5000/api";
const token = localStorage.getItem("token");

async function loadDashboard() {
    const res = await fetch(`${API}/dashboard/summary`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    const data = await res.json();

    document.getElementById("low").innerText = data.low_risk;
    document.getElementById("medium").innerText = data.medium_risk;
    document.getElementById("high").innerText = data.high_risk;
}

loadDashboard();