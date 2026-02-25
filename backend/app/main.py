from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <-- Import this
from backend.app.db.database import engine
from backend.app.models import models
from backend.app.api.v1 import users, auth, services, bookings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Service Booking System", version="1.0.0")

# --- ADD THIS CORS SECTION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for local development
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, POST, etc.
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(services.router, prefix="/api/v1/services", tags=["Services"])
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["Bookings"])

@app.get("/")
def read_root():
    return {"message": "API is online and ready for bookings!"}