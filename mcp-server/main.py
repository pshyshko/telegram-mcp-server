from mcp.server.fastmcp import FastMCP
from app.database.database import get_database_session, create_database, register_fixtures
from app.database.models import ReservationOrm, ReservationStatus
from datetime import datetime
from app.database.models import Base

mcp = FastMCP(
    name="Telegram Agents",
    host="0.0.0.0",
    port=8050,
    stateless_http=True,
)

@mcp.tool()
def get_all_free_reservations() -> str:
    """
    Retrieves all available free reservation slots from the database.

    Returns:
        str: A formatted string listing all free reservation slots, with each slot
            showing its ID and reservation time.
    """
    with get_database_session() as session:
        reservations = (
            session.query(ReservationOrm)
            .filter(ReservationOrm.status == ReservationStatus.FREE)
            .all()
        )

    output = ""
    for reservation in reservations:
        text_format = f"ID: {reservation.id} time {reservation.reservation_time}\n"
        output += text_format

    return output


@mcp.tool()
def make_free_reservation(reservation_time: datetime) -> str:
    """
    Creates a new reservation slot in the database and marks it as free.

    Args:
        reservation_time (datetime): The specific date and time for the new reservation slot.

    Returns:
        str: reservation_id of the created reservation.
    """
    with get_database_session() as session:
        new_reservation = ReservationOrm(
            reservation_time=reservation_time,
            employee_id=1,
            status=ReservationStatus.FREE,
        )
        session.add(new_reservation)
        session.commit()
        session.refresh(new_reservation)

    return f"Reservation id={str(new_reservation.id)}"


@mcp.tool()
def reserve_reservation(
    telegram_id: int, telegram_username: str, telegram_link: str, reservation_id: int
) -> str:
    """
    Reserves a free reservation slot for a user.

    Args:
        telegram_id (int): The Telegram ID of the user making the reservation.
        telegram_username (str): The Telegram username of the user.
        telegram_link (str): The Telegram link (e.g., t.me/username) of the user.
        reservation_id (int): The ID of the reservation slot to be reserved.

    Returns:
        str: A confirmation message, "Confirmed", if the reservation is successful.
            An error might be raised if the reservation ID is not found or the slot is not free.
    """
    with get_database_session() as session:
        reservations = (
            session.query(ReservationOrm)
            .filter(
                ReservationOrm.id == reservation_id,
                ReservationOrm.status == ReservationStatus.FREE,
            )
            .one()
        )

        reservations.telegram_id = telegram_id
        reservations.telegram_username = telegram_username
        reservations.telegram_link = telegram_link
        reservations.status = ReservationStatus.CONFIRMED
        session.commit()

    return "Success reservation"

if __name__ == "__main__":
    create_database(Base) 
    register_fixtures()
    mcp.run(transport="streamable-http")
