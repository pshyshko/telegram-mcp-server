from datetime import datetime

from enum import Enum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


class ReservationStatus(Enum):
    FREE = "FREE"
    CONFIRMED = "CONFIRMED"


class ReservationOrm(Base):
    __tablename__ = "reservations"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, index=True)
    reservation_time: Mapped[DateTime] = mapped_column(
        DateTime, index=True, default=datetime.now
    )
    telegram_id: Mapped[String] = mapped_column(String, nullable=True)
    telegram_username: Mapped[String] = mapped_column(String, nullable=True)
    telegram_link: Mapped[String] = mapped_column(String, nullable=True)

    employee_id: Mapped[Integer] = mapped_column(ForeignKey("employees.id"))
    employee: Mapped["EmployeeOrm"] = relationship(back_populates="reservations")
    status: Mapped[ReservationStatus] = mapped_column(
        nullable=False, default=ReservationStatus.FREE
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, index=True)
    username = mapped_column(String, unique=True, index=True, nullable=False)
    email = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    is_active = mapped_column(Boolean, default=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )


class EmployeeOrm(Base):
    __tablename__ = "employees"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, index=True)
    reservations: Mapped[list["ReservationOrm"]] = relationship(
        back_populates="employee"
    )
    first_name: Mapped[String] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    last_name: Mapped[String] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    employee_price: Mapped[Float] = mapped_column(Float)

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
