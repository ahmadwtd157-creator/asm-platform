async function login() {

const email = document.getElementById("email").value;
const password = document.getElementById("password").value;

if(!email || !password){
showToast("Warning","Email and password required","warning");
return;
}

try {

const res = await fetch(`${API_BASE_URL}/login`,{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({email,password})
});

const data = await res.json();

if(res.ok){
localStorage.setItem("token",data.token);
window.location.href="dashboard.html";
}else{
showToast("Login Failed",data.message || "Invalid credentials","danger");
}

}catch(err){
showToast("Error","Server unreachable","danger");
}

}

async function register(){

const email = document.getElementById("email").value;
const password = document.getElementById("password").value;

if(!email || !password){
alert("Email and password required");
return;
}

try{

const res = await fetch(`${API_BASE_URL}/register`,{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
email:email,
password:password
})

});

const data = await res.json();

if(res.ok){

alert("Account created successfully");

window.location.href="login.html";

}else{

alert(data.message || "Register failed");

}

}

catch(err){

console.error(err);
alert("Server error");

}

}

function logout(){
localStorage.removeItem("token");
window.location.href="login.html";
}

window.login = login;
window.register = register;
window.logout = logout;

function showToast(title,message,type="info"){

const colors={
success:"#28a745",
danger:"#dc3545",
warning:"#fd7e14",
info:"#17a2b8"
}

const toast=document.createElement("div");

toast.style.position="fixed";
toast.style.top="20px";
toast.style.right="20px";
toast.style.padding="12px 18px";
toast.style.color="white";
toast.style.backgroundColor=colors[type];
toast.style.borderRadius="6px";
toast.style.boxShadow="0 4px 10px rgba(0,0,0,0.4)";
toast.style.zIndex="9999";

toast.innerHTML=`<strong>${title}</strong><br>${message}`;

document.body.appendChild(toast);

setTimeout(()=>toast.remove(),3500);

}