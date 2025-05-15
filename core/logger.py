import os
import sys

from loguru import logger


os.makedirs("logs", exist_ok=True)

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

logger.add(
    "logs/scrapy_{time:YYYY-MM-DD}.log",
    level="INFO",
    rotation="1 GB",
    compression="zip",
    retention=5,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
