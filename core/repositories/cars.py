from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from loguru import logger
from core.models import Car
from core.repositories.postgres_base import get_db_session
from core.schemas.car_data import CarDataBase


class CarRepository:
    def __init__(self, session: Session) -> None:
        """
        Initialize the repository with an SQLAlchemy session.

        Args:
            session (Session): SQLAlchemy session for database operations.
        """
        self.session = session

    def get_car_by_url(self, url: str) -> Car | None:
        """
        Retrieve a Car object by its unique URL.

        Args:
            url (str): The URL of the car.

        Returns:
            Optional[Car]: The Car object if found, otherwise None.
        """
        return self.session.query(Car).filter_by(url=url).first()

    def save_car(self, car_data: CarDataBase) -> None:
        """
        Save or update a car record in the database.

        If a record with the given URL exists, updates its fields;
        otherwise, creates a new record.

        Args:
            car_data (CarDataBase): Car data as a Pydantic model.

        Raises:
            ValueError: If there is an error saving the car data.
        """
        existing_car = self.get_car_by_url(url=car_data.url)

        if existing_car:
            for key, value in car_data.model_dump(exclude_unset=True).items():
                setattr(existing_car, key, value)
        else:
            car_dict = car_data.model_dump()
            car = Car(**car_dict)

            try:
                self.session.add(car)
                self.session.commit()
            except SQLAlchemyError as e:
                self.session.rollback()
                logger.error(
                    f"Error saving car {car_data.url}: {str(e)}", exc_info=True
                )
                raise ValueError(f"Error saving car: {str(e)}")

    def add_car(self, car_data: CarDataBase) -> None:
        """
        Wrapper method to save a car.

        Args:
            car_data (CarDataBase): Car data.
        """
        self.save_car(car_data)


def get_car_repository() -> CarRepository:
    """
    Factory function to create a CarRepository instance.

    Uses a context manager to create a new database session.

    Returns:
        CarRepository: Repository instance with an active session.
    """
    with get_db_session() as session:
        return CarRepository(session=session)
