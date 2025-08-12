import logging
import os
from logging.handlers import RotatingFileHandler

from app.core.config import settings

# Create the log directory if it does not exist
log_dir = os.path.dirname(settings.LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Create handler for rotating file logging
file_handler = RotatingFileHandler(
    settings.LOG_FILE,
    maxBytes=5_000_000,  # 5 MB
    backupCount=5,  # Keep 5 backup files
    encoding="utf-8",
)
file_handler.setLevel(settings.LOG_LEVEL)
file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))

# Create handler for console logging
console_handler = logging.StreamHandler()
console_handler.setLevel(settings.LOG_LEVEL)
console_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))

# Configure the main logger
logger = logging.getLogger(settings.APP_NAME)
logger.setLevel(settings.LOG_LEVEL)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.propagate = (
    False  # Prevent log messages from being propagated to the root logger
)
