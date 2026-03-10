requireAuth();

async function loadDashboard(){

try{

const res = await fetch(`${API_BASE_URL}/dashboard/summary`,{
headers:getHeaders()
});

const data = await res.json();

document.getElementById("low").innerText = data.low || 0;
document.getElementById("medium").innerText = data.medium || 0;
document.getElementById("high").innerText = data.high || 0;

}
catch(err){

console.error("Dashboard error",err);

}

}

window.onload = function(){

loadDashboard();

setInterval(loadDashboard,5000);

}