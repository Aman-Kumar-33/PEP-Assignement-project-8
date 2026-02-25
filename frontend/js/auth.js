const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

// --- LOGIN LOGIC ---
document.getElementById("login-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = document.getElementById("login-btn");
  const originalText = btn.innerText;

  // UI Feedback: Loading state
  btn.innerText = "Authenticating...";
  btn.disabled = true;

  const formData = new URLSearchParams();
  formData.append("username", document.getElementById("email").value);
  formData.append("password", document.getElementById("password").value);

  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("token", data.access_token);
      window.location.href = "dashboard.html";
    } else {
      alert("Invalid email or password. Please try again.");
      btn.innerText = originalText;
      btn.disabled = false;
    }
  } catch (err) {
    alert("Server is offline. Please start the FastAPI backend.");
    btn.innerText = originalText;
    btn.disabled = false;
  }
});

// --- REGISTER LOGIC ---
document
  .getElementById("register-form")
  ?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const userData = {
      full_name: document.getElementById("full_name").value,
      email: document.getElementById("email").value,
      role: document.getElementById("role").value,
      password: document.getElementById("password").value,
    };

    try {
      const response = await fetch(`${API_BASE_URL}/users/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      });

      if (response.ok) {
        alert("Account created successfully! You can now log in.");
        window.location.href = "login.html";
      } else {
        const error = await response.json();
        alert("Registration failed: " + error.detail);
      }
    } catch (err) {
      console.error("Reg Error:", err);
    }
  });
