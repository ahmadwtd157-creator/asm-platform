requireAuth();

function getAssetId(){

const params = new URLSearchParams(window.location.search);

return params.get("id");

}

function riskBadge(level){

if(!level) return "secondary";

level = level.toLowerCase();

if(level === "high") return "danger";

if(level === "medium") return "warning";

if(level === "low") return "success";

return "secondary";

}

async function loadResults(){

const assetId = getAssetId();

try{

const res = await fetch(`${API_BASE_URL}/assets/${assetId}/results`,{

headers:getHeaders()

});

const data = await res.json();

const table = document.getElementById("resultsTable");

table.innerHTML = "";

if(!data.length){

table.innerHTML = `
<tr>
<td colspan="7" class="text-center">
No open ports detected
</td>
</tr>
`;

return;

}

data.forEach(r => {

const badge = riskBadge(r.criticality);

table.innerHTML += `

<tr>

<td>${r.port}</td>

<td>${r.service || ""}</td>

<td>${r.banner || ""}</td>

<td>${r.asset_type || ""}</td>

<td>${r.category || ""}</td>

<td>

<span class="badge badge-${badge}">
${r.criticality}
</span>

</td>

<td>${r.scan_date}</td>

</tr>

`;

});

}

catch(err){

console.error(err);

}

}

window.onload = loadResults;