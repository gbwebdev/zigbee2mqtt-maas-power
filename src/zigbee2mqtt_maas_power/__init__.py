import logging
import os

def configure_logger(log_level=None):
    """
    Configures the application logger.
    Log level can be set via CLI, config file, or environment variable.
    """
    # Default log level
    default_level = logging.INFO

    # Convert log level to logging module's constants
    log_level = log_level or default_level
    if isinstance(log_level, str):
        log_level = getattr(logging, log_level.upper(), default_level)

    # Configure the root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()  # Log to console
        ]
    )
    
    # If running under Gunicorn, integrate with Gunicorn's logger
    if "gunicorn" in os.environ.get("SERVER_SOFTWARE", "").lower():
        gunicorn_logger = logging.getLogger("gunicorn.error")
        logging.getLogger().handlers = gunicorn_logger.handlers
        logging.getLogger().setLevel(gunicorn_logger.level)

    # Log the configured log level
    logging.getLogger().info("Logger initialized with level: %s", logging.getLevelName(log_level))
    return logging.getLogger()