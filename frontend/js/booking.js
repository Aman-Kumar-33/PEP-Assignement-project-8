const API_BASE_URL = "http://127.0.0.1:8000/api/v1";
const urlParams = new URLSearchParams(window.location.search);
const serviceId = urlParams.get("id");

// Optional: Fetch service details to show the name on the card
async function loadServiceDetail() {
  try {
    const response = await fetch(`${API_BASE_URL}/services/`);
    const services = await response.json();
    const service = services.find((s) => s.id == serviceId);
    if (service) {
      document.getElementById("display-title").innerText = service.title;
    }
  } catch (err) {
    console.error("Could not load service details");
  }
}

document
  .getElementById("booking-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");
    if (!token) {
      alert("Session expired. Please login again.");
      window.location.href = "login.html";
      return;
    }

    const bookingData = {
      service_id: parseInt(serviceId),
      start_time: document.getElementById("start_time").value,
      end_time: document.getElementById("end_time").value,
    };

    try {
      const response = await fetch(`${API_BASE_URL}/bookings/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(bookingData),
      });

      if (response.ok) {
        alert("Success! Your booking is now pending.");
        window.location.href = "dashboard.html";
      } else {
        const errorData = await response.json();
        // Handle the "Already Booked" error specifically
        if (
          errorData.detail ===
          "This time slot is already booked with this provider."
        ) {
          alert(
            "⚠️ Conflict: This provider is already busy during this time. Please try a different slot.",
          );
        } else {
          alert("Error: " + errorData.detail);
        }
      }
    } catch (err) {
      alert("Failed to connect to server.");
    }
  });

loadServiceDetail();
