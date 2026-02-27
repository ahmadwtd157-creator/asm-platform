async function loadDashboard() {

    const summary = await apiGet("/dashboard/summary");

    if (!summary) return;

    document.getElementById("totalAssets").innerText = summary.total_assets;
    document.getElementById("lowRisk").innerText = summary.low;
    document.getElementById("mediumRisk").innerText = summary.medium;
    document.getElementById("highRisk").innerText = summary.high;

    const ctx = document.getElementById("riskChart").getContext("2d");

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Low', 'Medium', 'High'],
            datasets: [{
                data: [summary.low, summary.medium, summary.high]
            }]
        }
    });
}