import re
import scrapy
from scrapy.http import Response
from loguru import logger

from core.repositories.cars import get_car_repository
from core.repositories.postgres_base import init_db
from core.schemas.car_data import CarDataBase


class AutoriaSpider(scrapy.Spider):
    """Spider for scraping used car listings from auto.ria.com."""

    name = "autoria_spider"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/uk/car/used/"]
    page = 1

    PRICE_CLEAN_RE = re.compile(r"\D")
    ODOMETER_RE = re.compile(r"(\d+)")
    PHOTOS_COUNT_RE = re.compile(r"(\d+)")

    def __init__(self, *args, **kwargs):
        """
        Initialize the AutoriaSpider.

        Sets up the database connection and car repository.
        """
        super().__init__(*args, **kwargs)
        init_db()
        self.car_repository = get_car_repository()

    def parse(self, response: Response):  # noqa
        """
        Parse the listing page and extract car summaries.

        Follows each car link to extract detailed information.

        Args:
            response (Response): The response object from the listing page.

        Yields:
            Request: Scrapy requests for car detail pages.
        """
        try:
            for card in response.css("section.ticket-item"):
                url = card.css("a.m-link-ticket::attr(href)").get()
                image_url = card.css("a.photo-185x120 img::attr(src)").get()
                raw_price = card.css(
                    "div.price-ticket span.bold.size22.green::text"
                ).get()
                raw_odo = card.css("li.item-char.js-race::text").get()
                title = card.css("div.head-ticket a.address span.blue.bold::text").get()
                car_vin = card.css("span.label-vin span::text").get()

                item = {
                    "url": url,
                    "title": title,
                    "price_usd": self.parse_price_usd(raw_price=raw_price),
                    "odometer": self.parse_odometer(raw_odo=raw_odo),
                    "image_url": image_url,
                    "car_vin": car_vin,
                }

                if url:
                    logger.debug(f"Following car detail page: {url}")
                    yield response.follow(
                        url, callback=self.parse_car_page, meta={"item": item}
                    )

            if self.page < 5:
                self.page += 1
                next_page = f"https://auto.ria.com/uk/car/used/?page={self.page}"
                logger.info(f"Navigating to next listing page: {next_page}")
                yield response.follow(next_page, callback=self.parse)

        except Exception as e:
            logger.error(f"Error while parsing listing page: {e}", exc_info=True)

    def parse_car_page(self, response: Response):
        """
        Parse an individual car detail page and save the data to the database.

        Args:
            response (Response): The response object from the car detail page.

        Yields:
            dict: The scraped item (used mostly for logging/monitoring).
        """
        try:
            item = response.meta["item"]
            logger.info(f"Parsing car details page: {item['url']}")

            photos_text = response.css("a.show-all.link-dotted::text").get()
            if photos_text:
                match = self.PHOTOS_COUNT_RE.search(photos_text)
                item["photos_count"] = int(match.group(1)) if match else 0
            else:
                item["photos_count"] = 0

            car_number = (
                response.css("span.state-num.ua")
                .xpath("text()[1]")
                .get(default="")
                .strip()
            )
            item["car_number"] = car_number or None

            car_data = self.create_car_data(data=item)

            self.car_repository.add_car(car_data=car_data)
            logger.info(f"Car '{item['title']}' successfully saved to the database.")

            yield item

        except Exception as e:
            logger.error(f"Error while parsing car details page: {e}", exc_info=True)

    @staticmethod
    def parse_price_usd(raw_price: str) -> int | None:
        """
        Parse and clean the USD price from a raw price string.

        Args:
            raw_price (str): Raw price string (e.g. "$10 000").

        Returns:
            int | None: Parsed price in USD, or None if invalid.
        """
        if not raw_price:
            return None
        digits = re.sub(r"\D", "", raw_price)
        return int(digits) if digits else None

    @staticmethod
    def parse_odometer(raw_odo: str) -> int | None:
        """
        Parse and clean the odometer reading from a raw string.

        Args:
            raw_odo (str): Raw odometer string (e.g. "135 тис. км").

        Returns:
            int | None: Parsed odometer in kilometers, or None if invalid.
        """
        if not raw_odo:
            return None
        raw_odo = raw_odo.replace(" ", "")
        match = re.search(r"(\d+)", raw_odo)
        if not match:
            return None
        number = int(match.group(1))
        return number * 1000 if "тис" in raw_odo else number

    @staticmethod
    def create_car_data(data: dict) -> CarDataBase:
        """
        Convert a dictionary of parsed data into a CarDataBase instance.

        Args:
            data (dict): Parsed data dictionary from listing and detail page.

        Returns:
            CarDataBase: A structured data object ready to be saved in the database.
        """
        return CarDataBase(
            url=data["url"],
            title=data["title"],
            price_usd=data["price_usd"],
            odometer=data["odometer"],
            image_url=data["image_url"],
            car_vin=data["car_vin"],
            car_number=data["car_number"],
            photos_count=data["photos_count"],
        )
