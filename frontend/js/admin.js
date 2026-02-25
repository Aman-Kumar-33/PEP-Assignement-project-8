const API_BASE_URL = "http://127.0.0.1:8000/api/v1";
const token = localStorage.getItem("token");

async function loadAllBookings() {
  if (!token) {
    alert("Access Denied: No Admin Token Found");
    return;
  }

  try {
    // We fetch ALL bookings (assuming your current user has admin/provider rights)
    const response = await fetch(`${API_BASE_URL}/bookings/my-bookings`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const bookings = await response.json();

    const tbody = document.getElementById("admin-booking-rows");
    tbody.innerHTML = "";

    bookings.forEach((b) => {
      const row = document.createElement("tr");
      row.innerHTML = `
                <td>#${b.id}</td>
                <td><strong>Service ID: ${b.service_id}</strong></td>
                <td>${new Date(b.start_time).toLocaleString()}</td>
                <td><span class="status-pill ${b.status}">${b.status}</span></td>
                <td class="action-btns">
                    ${
                      b.status === "pending"
                        ? `
                        <button onclick="updateStatus(${b.id}, 'confirmed')" class="btn-primary" style="padding: 5px 10px; background: #059669;">Approve</button>
                        <button onclick="updateStatus(${b.id}, 'cancelled')" class="btn-outline" style="padding: 5px 10px; color: #dc2626;">Reject</button>
                    `
                        : '<span style="color:#94a3b8; font-size:0.8rem;">No Actions Available</span>'
                    }
                </td>
            `;
      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("Admin Fetch Error:", err);
  }
}

async function updateStatus(bookingId, newStatus) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/bookings/${bookingId}/status?new_status=${newStatus}`,
      {
        method: "PATCH",
        headers: { Authorization: `Bearer ${token}` },
      },
    );

    if (response.ok) {
      loadAllBookings(); // Refresh the list
    } else {
      alert("Failed to update status.");
    }
  } catch (err) {
    console.error("Status Update Error:", err);
  }
}

window.onload = loadAllBookings;
