requireAuth();

async function loadAssets() {

    try {

        const res = await fetch(`${API_BASE_URL}/assets`, {
            headers: getHeaders()
        });

        const data = await res.json();

        const table = document.getElementById("assetsTable");

        if (!table) {
            console.error("assetsTable element not found");
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

            <button class="btn btn-danger btn-sm"
            onclick="deleteAsset(${asset.id})">
            Delete
            </button>

            </td>

            </tr>
            `;
        });

    }

    catch (err) {

        console.error("Assets error:", err);

        alert("Cannot fetch assets");

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


async function deleteAsset(id) {

    if (!confirm("Delete this asset?")) return;

    await fetch(`${API_BASE_URL}/assets/${id}`, {

        method: "DELETE",

        headers: getHeaders()

    });

    loadAssets();
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


window.onload = loadAssets;