from . import *

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[0;36m',  # Cyan
        'INFO': '\033[0;32m',   # Green
        'WARNING': '\033[0;33m',  # Yellow
        'ERROR': '\033[0;31m',   # Red
        'CRITICAL': '\033[0;35m',  # Magenta
        'RESET': '\033[0m',      # Reset
    }

    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, self.COLORS['RESET'])}{log_message}{self.COLORS['RESET']}"

def setup_logger():
    logger = logging.getLogger('crossreads_petrography')
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Prevent propagation to root logger

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    handler = logging.StreamHandler()
    formatter = ColoredFormatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

logger = setup_logger()
logger.setLevel(logging.INFO)