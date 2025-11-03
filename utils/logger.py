import logging
import sys

def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
    Sets up a logger with consistent formatting.
    Logs to both console (stdout) and can be extended to file logging if needed.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent adding multiple handlers if called multiple times
    if not logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
