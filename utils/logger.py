import logging
import sys

def setup_logger(name: str = "travel_agent", level: int = logging.INFO):
    """
    Sets up a logger with the specified name and level.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Ensure stdout is using utf-8 encoding to avoid UnicodeEncodeError on Windows
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            # For older python versions where reconfigure might not exist, ignore
            pass

    # Check if handlers are already added to avoid duplicates
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        file_handler = logging.FileHandler("travel_agent.log", encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
