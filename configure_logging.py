import argparse
import sys

from loguru import logger

AVAILABLE_LOGGING_LEVELS = ("TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL")


def configure_logger() -> None:
    """Configuring bot logger level"""

    # Construct the argument parser
    ap = argparse.ArgumentParser(description='Telegram bot which returns weather forecast.')

    # Add the arguments to the parser
    ap.add_argument("--level", required=False, help="Logging level to set.")
    logger.debug("Getting list of arguments passed to app on startup")
    args = vars(ap.parse_args())
    logger.debug(f"Lst of arguments passed to app on startup: {args}")
    logger.info("Configuring application logger level...")
    # logger options
    log_format = "<b><light-green>{time:YYYY-MM-DD HH:mm:ss.SSS}</light-green> <YELLOW><black>{level: ^8}</black></YELLOW></b> <fg #c75e22>{name: ^15}:{line: >3}:</fg #c75e22> <green>{message}</green>"
    if not args:
        log_level = "INFO"
    elif isinstance(args, dict) and args['level'] in AVAILABLE_LOGGING_LEVELS:
        log_level = args['level']
    else:
        logger.error(
            f"Unable to apply logging level '{args['level']}' as it is absent among list of available logging levels:"
            f"\n{AVAILABLE_LOGGING_LEVELS}")
        raise RuntimeError
    # setting application logger parameters
    logger_config = {
        "handlers": [
            {"sink": sys.stdout, "level": log_level, "format": log_format, "colorize": True},
            {"sink": "logs/log_{time},log", "level": log_level, "format": log_format, "colorize": True, "rotation": "100 MB",
             "retention": "3 days"}
        ]
    }
    logger.configure(**logger_config)
