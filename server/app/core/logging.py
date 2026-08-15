# app/core/logging.py
from enum import Enum
import logging
import sys
from types import FrameType
from loguru import logger

from app.core import settings

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{extra[log_type]} | </cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


class LogType(str, Enum):
    APP = "app"
    DB_TRANSACTION = "db_transaction"
    AUTH = "auth"


class InterceptHandler(logging.Handler):

    def emit(self, record: logging.LogRecord) -> None:
        level: str | int

        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame: FrameType | None = sys._getframe(6)
        depth = 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging():
    logger.remove()

    logger.configure(
        extra={
            "log_type": LogType.APP,
        }
    )

    logger.add(
        sys.stdout,
        level="DEBUG" if settings.DEBUG else "INFO",
        diagnose=settings.DEBUG,
        colorize=True,
        format=LOG_FORMAT,
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    for name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"):
        logging_logger = logging.getLogger(name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.propagate = False
