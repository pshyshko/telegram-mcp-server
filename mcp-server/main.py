from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from app.database.database import create_database, get_database_session
from app.database.models import Base, ReservationOrm, ReservationStatus
from app.schemas.schemas import ReservationOut
from datetime import datetime

load_dotenv(".env")


mcp = FastMCP(
    name="Telegram Agents",
    host="0.0.0.0",
    port=8050,
    stateless_http=True,
)

@mcp.tool()
def get_all_free_reservations() -> list[ReservationOut]:
    """Get all free reservations"""
    with get_database_session() as session:
        reservations = (
            session.query(ReservationOrm)
            .filter(
                ReservationOrm.status == ReservationStatus.FREE,
            )
            .all()
        )

    output = [ReservationOut.model_validate(item) for item in reservations]
    return output


@mcp.tool()
def create_free_reservation(
    reservation_time: datetime,
    employee_id: int,
) -> ReservationOut:
    with get_database_session() as session:
        new_reservation = ReservationOrm(
            reservation_time=reservation_time,
            employee_id=employee_id,
            status=ReservationStatus.FREE,
        )
        session.add(new_reservation)
        session.commit()
        session.refresh(new_reservation) # Refresh to get the ID and timestamps

    return ReservationOut.model_validate(new_reservation)


if __name__ == "__main__":
    create_database(Base)
    mcp.run(transport="sse")
