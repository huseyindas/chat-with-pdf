import sys
import logging

from core.config import settings


logger = logging.getLogger(__name__)

if settings.debug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.ERROR)

stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)
