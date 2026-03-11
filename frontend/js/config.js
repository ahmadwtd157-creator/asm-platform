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

function showToast(title, message, type="success"){

    const colors = {
        success: "bg-success",
        danger: "bg-danger",
        warning: "bg-warning",
        info: "bg-info"
    };

    const toastHTML = `
    <div class="toast ${colors[type]}" role="alert" data-delay="3000">
        <div class="toast-header">
            <strong class="mr-auto">${title}</strong>
            <button type="button" class="ml-2 mb-1 close" data-dismiss="toast">
                <span>&times;</span>
            </button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    </div>
    `;

    const container = document.getElementById("toastContainer");

    container.insertAdjacentHTML("beforeend", toastHTML);

    $('.toast').toast('show');
}