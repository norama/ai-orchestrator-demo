import logging

from app.settings import env_settings


def setup_logging() -> None:
    logging.basicConfig(
        level=env_settings.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
