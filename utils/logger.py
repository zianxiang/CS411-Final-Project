import logging

def configure_logger(logger):
    """
    Configures the logger with a standard format and level.
    Args:
        logger (logging.Logger): The logger instance to configure.
    """
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
