import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler


def setup_logging(filename):
    log_dir = os.getenv("LOG_DIR")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{filename}.log")

    # Get log level from env, default to INFO
    log_level_str = os.getenv("LOG_LEVEL").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, delay=True, backupCount=90, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    file_handler.suffix = "%Y-%m-%d.log"

    # Stdout Handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)

    logging.basicConfig(level=log_level, handlers=[file_handler, stream_handler])