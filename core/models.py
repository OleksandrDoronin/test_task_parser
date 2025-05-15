from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from core.repositories.postgres_base import Base


class Car(Base):
    __tablename__ = "car_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    url: Mapped[str | None] = mapped_column(String, nullable=False, unique=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    price_usd: Mapped[int | None] = mapped_column(Integer, nullable=True)
    odometer: Mapped[int | None] = mapped_column(Integer, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    car_vin: Mapped[str | None] = mapped_column(String, nullable=True)
    photos_count: Mapped[int | None] = mapped_column(Integer, default=0)
    car_number: Mapped[str | None] = mapped_column(String, nullable=True)
    datetime_found: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
