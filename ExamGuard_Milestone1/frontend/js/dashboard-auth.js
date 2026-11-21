
(async function protectDashboard() {
  const token = localStorage.getItem("examguard_access_token");
  if (!token) {
    window.location.replace("login.html");
    return;
  }
  try {
    const response = await fetch("http://127.0.0.1:8000/auth/me", {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!response.ok) throw new Error("Session expired");
    const user = await response.json();
    const page = location.pathname.split("/").pop();
    const requiredRole = {
      "candidate-dashboard.html": "candidate",
      "invigilator-dashboard.html": "invigilator",
      "admin-dashboard.html": "administrator"
    }[page];

    if (requiredRole && user.role !== requiredRole) {
      throw new Error("You do not have access to this dashboard");
    }
    localStorage.setItem("examguard_user", JSON.stringify(user));
    document.documentElement.classList.add("authenticated");
  } catch (error) {
    localStorage.removeItem("examguard_access_token");
    localStorage.removeItem("examguard_user");
    alert(error.message || "Please sign in again.");
    window.location.replace("login.html");
  }
})();

function examGuardLogout() {
  localStorage.removeItem("examguard_access_token");
  localStorage.removeItem("examguard_user");
  window.location.href = "login.html";
}
