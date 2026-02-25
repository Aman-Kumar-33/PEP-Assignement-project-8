const API_BASE_URL = "http://127.0.0.1:8000/api/v1";
const token = localStorage.getItem("token");

async function loadDashboard() {
  if (!token) {
    window.location.href = "login.html";
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/bookings/my-bookings`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) throw new Error("Failed to fetch bookings");

    const bookings = await response.json();

    // 1. Update the Stats Counters
    document.getElementById("total-count").innerText = bookings.length;
    document.getElementById("upcoming-count").innerText = bookings.filter(
      (b) => b.status === "confirmed",
    ).length;

    const list = document.getElementById("bookings-list");

    // 2. Check if we have data
    if (bookings.length === 0) {
      list.innerHTML = `
                <div class="empty-state">
                    <p style="font-size: 1.2rem; color: #94a3b8; margin-bottom: 20px;">No bookings found yet.</p>
                    <a href="index.html" class="btn-primary">Find a Service</a>
                </div>`;
      return;
    }

    // 3. Clear and Inject Booking Cards
    list.innerHTML = "";
    bookings.forEach((b) => {
      const startDate = new Date(b.start_time);
      const card = document.createElement("div");
      card.className = "stat-card"; // Reusing your white card style
      card.style.borderLeft = `5px solid ${b.status === "confirmed" ? "#10b981" : "#f59e0b"}`;

      card.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:start;">
                    <div>
                        <h4 style="color: #6366f1; margin-bottom:5px;">Booking #${b.id}</h4>
                        <p style="font-size: 1.1rem; font-weight: 600; margin:0;">Service ID: ${b.service_id}</p>
                        <p style="color: #64748b; font-size: 0.9rem; margin-top:10px;">
                            📅 ${startDate.toLocaleDateString()} <br>
                            ⏰ ${startDate.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                        </p>
                    </div>
                    <span style="
                        padding: 5px 12px; 
                        border-radius: 20px; 
                        font-size: 0.7rem; 
                        font-weight: bold; 
                        text-transform: uppercase;
                        background: ${b.status === "confirmed" ? "#d1fae5" : "#fef3c7"};
                        color: ${b.status === "confirmed" ? "#065f46" : "#92400e"};
                    ">
                        ${b.status}
                    </span>
                </div>
            `;
      list.appendChild(card);
    });
  } catch (err) {
    console.error("Dashboard Error:", err);
    document.getElementById("bookings-list").innerHTML =
      `<p style="color:red">Error connecting to server. Is the backend running?</p>`;
  }
}

window.onload = loadDashboard;
