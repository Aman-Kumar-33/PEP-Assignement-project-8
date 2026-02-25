# Online Service Booking & Management System

A robust, full-stack web application designed to streamline the connection between service providers and customers. This system features a professional booking engine, role-based access control, and a modern dashboard interface.

---

## 🎯 Project Purpose

The primary goal of this project is to solve the **"Overlap Problem"** in scheduling.

In real-world service industries, manual scheduling often leads to:
- Double bookings  
- Administrative errors  
- Miscommunication between providers and customers  

This application automates the process by:

### ✅ Preventing Double Bookings
A backend engine mathematically ensures no provider is booked for two services at the same time.

### ✅ Providing Transparency
Customers can track their booking status, and providers can manage their availability through a secure administrative portal.

### ✅ Ensuring Security
Implementation of **JWT (JSON Web Tokens)** ensures that user data and booking schedules remain protected and private.

---

## ⚙️ How the Code Works

The project follows a **decoupled architecture** with:

- **Backend:** Python FastAPI
- **Frontend:** Vanilla JavaScript & CSS

---

## 🧠 1. The Backend (The "Brain")

### 🔹 FastAPI & Uvicorn
Handles high-performance asynchronous HTTP requests.

### 🔹 SQLAlchemy (ORM)
Manages database logic using Python classes instead of writing raw SQL queries.

### 🔹 Conflict Detection Logic
The core scheduling algorithm prevents overlap using:

```
(ExistingStart < NewEnd) AND (ExistingEnd > NewStart)
```

If this condition is true, the booking request is rejected.

### 🔹 Authentication & Security
- **Passlib** securely hashes user passwords.
- **OAuth2 + JWT** manages authentication and session persistence.

---

## 🖥️ 2. The Frontend (The "Body")

### 🔹 Dynamic Rendering
JavaScript fetches JSON data from the API and dynamically builds UI components.

### 🔹 State Management
`localStorage` stores the user's JWT token to maintain login state across pages.

### 🔹 Responsive Design
A custom CSS framework provides:
- Sidebar-driven dashboard
- Glassmorphism card effects
- Clean and premium user experience

---

## 🚀 How to Run the Program

Follow these steps to run the project locally.

---

## 📌 Prerequisites

- Python 3.8+
- A code editor (e.g., VS Code)

---

## 🛠️ Step 1: Set Up the Backend

### 1️⃣ Navigate to the project root directory.

### 2️⃣ Create a virtual environment:

```bash
python -m venv venv
```

### 3️⃣ Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4️⃣ Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy pydantic passlib pyjwt
```

### 5️⃣ Start the backend server:

```bash
uvicorn backend.app.main:app --reload
```

---

## 🌱 Step 2: Seed the Database

To populate categories and services:

```bash
python -m backend.seed
```

This prevents the system from starting with an empty database.

---

## 🌐 Step 3: Launch the Frontend

1. Keep the backend terminal running.
2. Open `frontend/index.html` in your browser.

💡 Recommended: Use the **Live Server extension** in VS Code.

### Default Credentials (Seeded)

```
Email: pro@example.com
Password: password123
```

Or register a new account.

---

## 🔐 Step 4: Access the Admin Portal (Secret)

To manage system-wide bookings, manually navigate to:

```
http://127.0.0.1:5500/admin-portal.html
```

(Port may vary depending on your Live Server configuration.)

---

## 📦 Architecture Summary

| Layer      | Technology Used        | Purpose |
|------------|------------------------|----------|
| Backend    | FastAPI + SQLAlchemy   | API & Database Management |
| Auth       | Passlib + JWT          | Secure Authentication |
| Frontend   | HTML + CSS + JS        | UI & User Interaction |
| Server     | Uvicorn                | ASGI Server |

---

## 🏁 Conclusion

This system demonstrates:

- Clean separation of frontend and backend
- Secure authentication implementation
- Mathematical prevention of scheduling conflicts
- Professional dashboard architecture

It serves as a strong foundation for scaling into:
- Payment integration
- Multi-provider support
- Advanced analytics dashboards
- Mobile application support
