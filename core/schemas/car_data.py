from datetime import datetime

from pydantic import BaseModel, Field


class CarDataBase(BaseModel):
    """
    Represents car listing data including details like price, mileage,
    VIN, photos count, and the datetime when the data was found.
    """

    url: str | None = None
    title: str | None = None
    price_usd: int | None = None
    odometer: int | None = None
    image_url: str | None = None
    car_vin: str | None = None
    photos_count: int | None = 0
    car_number: str | None = None
    datetime_found: datetime = Field(default_factory=datetime.now)
