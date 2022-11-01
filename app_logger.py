from config import LOG_FOLDER, LOG_FORMAT, LOG_FILE, LOG_MAX_BYTES, LOG_COUNT
from pathlib import Path
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import traceback

log_dir = Path(LOG_FOLDER)
log_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
log_formatter = logging.Formatter(LOG_FORMAT)
file_handler = RotatingFileHandler(os.path.join(LOG_FOLDER, LOG_FILE), maxBytes=LOG_MAX_BYTES, backupCount=LOG_COUNT)
file_handler.setFormatter(log_formatter)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def logger_output(message, debug_mode, error_level):
    lf = '\n'
    error_message = f'{traceback.format_exc().replace(lf, " ")} : {message}' if debug_mode is True else f'{str(message)}'
    if error_level == 'error':
        logger.error(error_message)
    elif error_level == 'warning':
        logger.warning(f'{message}')
    elif error_level == 'info':
        logger.info(error_message)
