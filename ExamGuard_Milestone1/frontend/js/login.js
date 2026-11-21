
const passwordInput = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");
if (togglePassword) {
  togglePassword.addEventListener("click", () => {
    const show = passwordInput.type === "password";
    passwordInput.type = show ? "text" : "password";
    togglePassword.textContent = show ? "Hide" : "Show";
  });
}

const loginForm = document.getElementById("loginForm");
const loginMessage = document.getElementById("loginMessage");
const API_BASE = "http://127.0.0.1:8000";

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const role = document.getElementById("role").value;
  const email = document.getElementById("email").value.trim();
  const password = passwordInput.value;

  if (!role) {
    loginMessage.textContent = "Please select your role.";
    return;
  }

  const button = loginForm.querySelector('button[type="submit"]');
  button.disabled = true;
  loginMessage.textContent = "Signing in...";

  try {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, role })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Login failed");

    localStorage.setItem("examguard_access_token", data.access_token);
    localStorage.setItem("examguard_user", JSON.stringify(data.user));

    const destinations = {
      candidate: "candidate-dashboard.html",
      invigilator: "invigilator-dashboard.html",
      administrator: "admin-dashboard.html"
    };
    window.location.href = destinations[data.user.role];
  } catch (error) {
    loginMessage.textContent = error.message || "Unable to connect to the server.";
  } finally {
    button.disabled = false;
  }
});
