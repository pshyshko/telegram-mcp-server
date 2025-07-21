import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# Enum from your SQLAlchemy model, to be used in Pydantic models
class ReservationStatus(str, enum.Enum):
    """
    Enum for the status of a reservation.
    Mirrors the SQLAlchemy model's enum.
    """
    FREE = "FREE"
    CONFIRMED = "CONFIRMED"


# ===================================================================
# Pydantic Models for EmployeeOrm
# ===================================================================

class EmployeeBase(BaseModel):
    first_name: str = Field(..., description="Employee's first name", example="John")
    last_name: str = Field(..., description="Employee's last name", example="Doe")
    employee_price: float = Field(..., description="Price associated with the employee", example=150.50)


class EmployeeIn(EmployeeBase):
    reservation_id: int = Field(..., description="The ID of the parent reservation")


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, description="Employee's first name", example="Jane")
    last_name: Optional[str] = Field(None, description="Employee's last name", example="Smith")
    employee_price: Optional[float] = Field(None, description="Price associated with the employee", example=175.00)


class EmployeeOut(EmployeeBase):
    id: int = Field(..., description="Unique identifier for the employee")
    created_at: datetime = Field(..., description="Timestamp of employee creation")
    updated_at: datetime = Field(..., description="Timestamp of last employee update")

    model_config = ConfigDict(from_attributes=True)

class ReservationBase(BaseModel):
    reservation_time: datetime = Field(..., description="The scheduled time for the reservation")
    status: ReservationStatus = Field(default=ReservationStatus.FREE, description="The current status of the reservation")
    telegram_id: Optional[str] = Field(None, description="User's Telegram ID", example="123456789")
    telegram_username: Optional[str] = Field(None, description="User's Telegram username", example="john_doe")
    telegram_link: Optional[str] = Field(None, description="Link to the user's Telegram profile", example="t.me/john_doe")

class ReservationIn(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    reservation_time: Optional[datetime] = Field(None, description="The scheduled time for the reservation")
    status: Optional[ReservationStatus] = Field(None, description="The new status of the reservation")
    telegram_id: Optional[str] = Field(None, description="User's Telegram ID", example="987654321")
    telegram_username: Optional[str] = Field(None, description="User's Telegram username", example="jane_smith")
    telegram_link: Optional[str] = Field(None, description="Link to the user's Telegram profile", example="t.me/jane_smith")


class ReservationOut(ReservationBase):
    id: int = Field(..., description="Unique identifier for the reservation")
    created_at: datetime = Field(..., description="Timestamp of reservation creation")
    updated_at: datetime = Field(..., description="Timestamp of last reservation update")
    
    employee: Optional[EmployeeOut] = Field(None, description="The employee associated with this reservation")

    model_config = ConfigDict(from_attributes=True)