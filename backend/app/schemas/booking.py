from pydantic import BaseModel
from datetime import datetime
from backend.app.models.models import BookingStatus

class BookingBase(BaseModel):
    service_id: int
    start_time: datetime
    end_time: datetime

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    customer_id: int
    status: BookingStatus

    class Config:
        from_attributes = True