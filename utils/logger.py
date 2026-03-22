import logging
from pathlib import Path


# Create logs directory if does not exists
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("logs/contact_book.log")],
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
