const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

async function fetchServices() {
  try {
    const response = await fetch(`${API_BASE_URL}/services/`);
    const services = await response.json();

    const grid = document.getElementById("services-grid");
    grid.innerHTML = ""; // Clear loading text

    if (services.length === 0) {
      grid.innerHTML = "<p>No services found. Be the first to add one!</p>";
      return;
    }

    services.forEach((service) => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
                <h3>${service.title}</h3>
                <p>${service.description}</p>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong>$${service.price}</strong>
                    <span>${service.duration_minutes} mins</span>
                </div>
                <br>
                <a href="booking.html?id=${service.id}" class="btn-primary">Book Now</a>
            `;
      grid.appendChild(card);
    });
  } catch (error) {
    console.error("Error fetching services:", error);
    document.getElementById("services-grid").innerHTML =
      "<p>Error loading services. Is the backend running?</p>";
  }
}

// Run the function when the page loads
window.onload = fetchServices;
