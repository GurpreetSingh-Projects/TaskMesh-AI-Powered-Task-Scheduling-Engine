import sys

from loguru import logger


def setup_logging():
    is_production = True

    logger.remove()

    logger.add(
        sys.stdout,
        level="DEBUG",
        colorize=True,
        enqueue=True,
        backtrace=False,
        diagnose=False,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
    )
