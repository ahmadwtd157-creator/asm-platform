requireAuth();

async function loadAssets(){

try{

const res = await fetch(`${API_BASE_URL}/assets`,{
headers:getHeaders()
});

if(res.status === 401){

showToast("Session expired","Please login again","danger");

localStorage.removeItem("token");

setTimeout(()=>{
window.location.href="login.html";
},1500);

return;
}

const data = await res.json();

if(!Array.isArray(data)){

console.error("Unexpected response:",data);

showToast("Error","Invalid API response","danger");

return;
}

const table = document.getElementById("assetsTable");

if(!table){
console.error("assetsTable not found");
return;
}

table.innerHTML = "";

data.forEach(asset => {

table.innerHTML += `
<tr>

<td>${asset.id}</td>

<td>${asset.domain || ""}</td>

<td>${asset.ip_address || ""}</td>

<td>

<a href="asset_details.html?id=${asset.id}" 
class="btn btn-info btn-sm">
Details
</a>

<button class="btn btn-warning btn-sm"
onclick="scanAsset(${asset.id})">
Scan
</button>

<button class="btn btn-primary btn-sm"
onclick="discoverAsset(${asset.id})">
Discover
</button>

<button class="btn btn-danger btn-sm"
onclick="deleteAsset(${asset.id})">
Delete
</button>

</td>
</tr>
`;

});

}catch(err){

console.error("Assets fetch error:",err);

showToast("Error","Cannot load assets","danger");

}

}


async function addAsset() {

    const domain = document.getElementById("domain").value;
    const ip = document.getElementById("ip").value;

    await fetch(`${API_BASE_URL}/assets`, {

        method: "POST",

        headers: getHeaders(),

        body: JSON.stringify({
            domain: domain,
            ip_address: ip
        })

    });

    loadAssets();
}

async function deleteAsset(id){

if(!confirm("Delete this asset?")) return;

try{

const res = await fetch(`${API_BASE_URL}/assets/${id}`,{
method:"DELETE",
headers:getHeaders()
});

if(!res.ok){

const text = await res.text();
console.error("Delete error:",text);

showToast("Error","Delete failed","danger");
return;

}

const data = await res.json();

showToast("Success",data.message,"success");

loadAssets();

}catch(err){

console.error("Network error:",err);

showToast("Error","Network error","danger");

}

}

async function scanAsset(id){

    try{

        showToast("Scan", "Scan started...", "info");

        const res = await fetch(`${API_BASE_URL}/assets/${id}/scan`,{
            method:"POST",
            headers:getHeaders()
        });

        const data = await res.json();

        showToast("Scan Completed", data.message, "success");

    }

    catch(err){

        showToast("Error", "Scan failed", "danger");

    }

}

async function discoverAsset(id){

try{

showToast("Discovery","Starting subdomain discovery...","info");

const res = await fetch(`${API_BASE_URL}/discover/${id}`,{
method:"POST",
headers:getHeaders()
});

const data = await res.json();

showToast("Discovery Completed",
`Found ${data.discovered} new subdomains`,
"success");

loadAssets();

}
catch(err){

showToast("Error","Discovery failed","danger");

}

}


window.onload = loadAssets;