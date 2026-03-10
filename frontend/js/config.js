const API_BASE_URL = "http://localhost:5000/api";

function getToken() {
    return localStorage.getItem("token");
}

function getHeaders() {
    return {
        "Authorization": `Bearer ${getToken()}`,
        "Content-Type": "application/json"
    };
}

function requireAuth() {
    if (!getToken()) {
        window.location.href = "login.html";
    }
}