import logging
from logging.handlers import TimedRotatingFileHandler

def get_logger():
    logger = logging.getLogger("fastapi_app")
    
    # Check if the logger already has handlers to avoid duplicates
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Create a handler that writes log messages to a file, rotating every 7 days
        handler = TimedRotatingFileHandler("logs/fastapi_app.log", when="D", interval=7, backupCount=4)
        handler.setLevel(logging.DEBUG)

        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(handler)

        # Prevent the logger from propagating messages to the root logger
        logger.propagate = False

    return logger