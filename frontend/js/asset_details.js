requireAuth();

function getAssetId(){

    const params = new URLSearchParams(window.location.search);

    return params.get("id");

}


/*
Professional Port Risk Classification
Based on common attack surface exposure
*/

function classifyPortRisk(port){

    port = Number(port);

    const criticalPorts = [
        21,   // FTP
        22,   // SSH
        23,   // Telnet
        25,   // SMTP
        110,  // POP3
        143,  // IMAP
        445,  // SMB
        1433, // MSSQL
        1521, // Oracle
        2049, // NFS
        2181, // Zookeeper
        2375, // Docker
        2376, // Docker TLS
        2483, // Oracle
        2484, // Oracle
        3000, // Dev servers
        3306, // MySQL
        3389, // RDP
        4444, // Metasploit
        5432, // PostgreSQL
        5601, // Kibana
        5900, // VNC
        5985, // WinRM
        5986, // WinRM SSL
        6379, // Redis
        6667, // IRC
        7001, // Weblogic
        7002, // Weblogic SSL
        8000,
        8008,
        8080,
        8081,
        8088,
        8090,
        8443,
        8888,
        9000,
        9042, // Cassandra
        9090,
        9200, // Elasticsearch
        9418  // Git
    ];

    const mediumPorts = [
        53,   // DNS
        69,   // TFTP
        111,  // RPC
        123,  // NTP
        161,  // SNMP
        389,  // LDAP
        636,  // LDAPS
        989,
        990,
        1025,
        1434,
        1524,
        1812,
        1813,
        2082,
        2083,
        2086,
        2087,
        2095,
        2096,
        2100,
        2222,
        2601,
        2604,
        2605,
        2607,
        2608,
        2809,
        3128,
        4443,
        4848,
        5060,
        5061,
        5222,
        5269,
        5357,
        5358
    ];

    if (criticalPorts.includes(port)) return "high";

    if (mediumPorts.includes(port)) return "medium";

    return "low";
}


function getRiskColor(risk){

    if(risk === "high") return "danger";

    if(risk === "medium") return "warning";

    return "success";

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
            <td colspan="5" class="text-center">
            No open ports detected
            </td>
            </tr>
            `;

            return;
        }

        data.forEach(r => {

            const risk = classifyPortRisk(r.port);

            const color = getRiskColor(risk);

            table.innerHTML += `

            <tr>

            <td>${r.port}</td>

            <td>${r.service || ""}</td>

            <td>${r.banner || ""}</td>

            <td>
            <span class="badge badge-success">
            open
            </span>
            </td>

            <td>
            <span class="badge badge-${color}">
            ${risk}
            </span>
            </td>

            </tr>

            `;

        });

    }

    catch(err){

        console.error("Error loading results",err);

    }

}


window.onload = loadResults;