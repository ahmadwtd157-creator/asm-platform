const API = "http://localhost:5000/api";
const token = localStorage.getItem("token");

function authHeader() {
    return {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
    };
}

async function loadAssets() {
    const res = await fetch(`${API}/assets`, {
        headers: authHeader()
    });

    const data = await res.json();
    const table = document.getElementById("assetsTable");
    table.innerHTML = "";

    data.forEach(asset => {
        table.innerHTML += `
            <tr>
              <td>${asset.id}</td>
              <td>${asset.domain}</td>
              <td>${asset.ip_address}</td>
              <td>
                <button class="btn btn-sm btn-warning" onclick="scan(${asset.id})">Scan</button>
                <button class="btn btn-sm btn-info" onclick="view(${asset.id})">View</button>
                <button class="btn btn-sm btn-danger" onclick="removeAsset(${asset.id})">Delete</button>
              </td>
            </tr>
        `;
    });
}

async function addAsset() {
    const domain = document.getElementById("domain").value;
    const ip = document.getElementById("ip").value;

    await fetch(`${API}/assets`, {
        method: "POST",
        headers: authHeader(),
        body: JSON.stringify({ domain, ip_address: ip })
    });

    loadAssets();
}

async function removeAsset(id) {
    await fetch(`${API}/assets/${id}`, {
        method: "DELETE",
        headers: authHeader()
    });

    loadAssets();
}

async function scan(id) {
    await fetch(`${API}/assets/${id}/scan`, {
        method: "POST",
        headers: authHeader()
    });

    alert("Scan Completed");
}

function view(id) {
    window.location.href = `asset_details.html?id=${id}`;
}

loadAssets();
