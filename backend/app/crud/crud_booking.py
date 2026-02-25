from sqlalchemy.orm import Session
from sqlalchemy import and_

from backend.app.models import models
from backend.app.schemas import booking as booking_schema

# --- BOOKING LOGIC & OVERLAP CHECK ---

def check_overlap(db: Session, provider_id: int, start_time, end_time):
    """
    The Double-Booking Preventer!
    Checks if a provider has any existing bookings that overlap with the requested time.
    Overlap math: (existing_start < new_end) AND (existing_end > new_start)
    """
    overlapping_booking = db.query(models.Booking).join(models.Service).filter(
        # 1. It must be the same provider
        models.Service.provider_id == provider_id,
        # 2. We only care if the existing booking is pending or confirmed
        models.Booking.status.in_([models.BookingStatus.pending, models.BookingStatus.confirmed]),
        # 3. The time overlap math
        models.Booking.start_time < end_time,
        models.Booking.end_time > start_time
    ).first()
    
    return overlapping_booking is not None

def create_booking(db: Session, booking: booking_schema.BookingCreate, customer_id: int):
    """Create a new booking and attach the logged-in customer's ID."""
    db_booking = models.Booking(
        customer_id=customer_id,
        service_id=booking.service_id,
        start_time=booking.start_time,
        end_time=booking.end_time,
        status=models.BookingStatus.pending # Default status
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

# --- DASHBOARD QUERIES ---

def get_user_bookings(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Fetch all bookings made by a specific customer."""
    return db.query(models.Booking).filter(
        models.Booking.customer_id == user_id
    ).offset(skip).limit(limit).all()

def get_provider_bookings(db: Session, provider_id: int, skip: int = 0, limit: int = 100):
    """Fetch all bookings requested for a specific provider's services."""
    return db.query(models.Booking).join(models.Service).filter(
        models.Service.provider_id == provider_id
    ).offset(skip).limit(limit).all()

def update_booking_status(db: Session, booking_id: int, new_status: models.BookingStatus):
    """Allow providers/admins to accept, reject, or cancel a booking."""
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if db_booking:
        db_booking.status = new_status
        db.commit()
        db.refresh(db_booking)
    return db_booking