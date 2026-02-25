from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.schemas import booking as booking_schema
from backend.app.crud import crud_booking, crud_service
from backend.app.db.database import get_db
from backend.app.api.deps import get_current_user
from backend.app.models import models

router = APIRouter()

@router.post("/", response_model=booking_schema.BookingResponse)
def create_new_booking(
    booking: booking_schema.BookingCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a booking. Includes real-time validation to prevent double bookings.
    """
    # 1. Fetch the service to find out who the provider is
    service = crud_service.get_service_by_id(db, service_id=booking.service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    # 2. THE VALIDATION: Check for overlapping bookings
    is_overlapping = crud_booking.check_overlap(
        db, 
        provider_id=service.provider_id, 
        start_time=booking.start_time, 
        end_time=booking.end_time
    )
    
    if is_overlapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This time slot is already booked with this provider."
        )

    # 3. If no overlap, save the booking
    return crud_booking.create_booking(db=db, booking=booking, customer_id=current_user.id)

@router.get("/my-bookings", response_model=List[booking_schema.BookingResponse])
def get_my_bookings(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """Get all bookings made by the logged-in user."""
    return crud_booking.get_user_bookings(db, user_id=current_user.id)

@router.patch("/{booking_id}/status", response_model=booking_schema.BookingResponse)
def change_booking_status(
    booking_id: int, 
    new_status: models.BookingStatus,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Allow providers to Accept or Reject bookings."""
    # Logic check: Only the provider of the service should be able to change status
    # (Simplified for now - can be expanded later)
    return crud_booking.update_booking_status(db, booking_id=booking_id, new_status=new_status)