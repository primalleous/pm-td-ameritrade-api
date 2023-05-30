# pylint: disable=line-too-long
from datetime import datetime
from pathlib import Path
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from os import environ, getenv
import colorlog
from td.config import TdConfiguration

strftime_format = "%Y-%m-%d_%H-%M-%S"

log_formatting_str = "%(levelname)s: tdschwab-api %(asctime)s | %(filename)s line %(lineno)d |\n%(message)s"
colored_log_formatting_str = "%(log_color)s%(levelname)s%(reset)s: %(blue)s%(asctime)s%(reset)s | %(purple)s%(filename)s line %(lineno)d %(reset)s |\n%(white)s%(message)s"

log_formatter = logging.Formatter(log_formatting_str)
colored_log_formatter = colorlog.ColoredFormatter(
    colored_log_formatting_str,
    datefmt=None,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
    secondary_log_colors={},
    style="%",
)


def log_namer(log_path: Path):
    """
    Returns a Path object with the module and timestamp appended.

    Parameters:
    log_path (Path): The path of the log file.

    Returns:
    Path: A Path object with the module and timestamp appended.
    """

    module = os.path.basename(log_path)
    module = module[: module.find("_")]
    timestamp = datetime.now().strftime(strftime_format)
    module_str = module + "_" + timestamp + ".txt"

    return Path(log_path).parent / module_str


def initialize_file_log(log_name, log_root_path_, td_api_debug):
    """
    Initializes and returns a TimedRotatingFileHandler for logging to a file.

    Parameters:
    log_name (str): The name of the log file.
    log_root_path_ (str): The path of the log directory.
    td_api_debug (bool): Whether TD API debugging is enabled.

    Returns:
    TimedRotatingFileHandler: A TimedRotatingFileHandler object for logging to a file.
    """

    log_root_path = Path(log_root_path_)
    log_module_path = log_root_path / log_name

    if not log_root_path.exists():
        log_root_path.mkdir()

    if not log_module_path.exists():
        log_module_path.mkdir()

    log_handler_file = TimedRotatingFileHandler(
        str(
            log_module_path
            / f"{log_name}_{datetime.now().strftime(strftime_format)}.txt"
        ),
        when="M",
        interval=30,
        encoding="utf-8",
    )

    if td_api_debug:
        log_handler_file.setLevel(logging.DEBUG)
    else:
        log_handler_file.setLevel(logging.INFO)

    log_handler_file.setFormatter(log_formatter)
    log_handler_file.namer = log_namer

    return log_handler_file


class TdLogger:
    """
    A class for logging messages to the console and a file.

    Class Attributes:
    _config (TdConfiguration): An instance of TdConfiguration.
    app_name (str): The name of the application.
    class_logger (Logger): An instance of the logging.Logger class for logging messages.
    config_present (bool): Whether the configuration file is present.
    log_root_path (str): The path of the log directory.
    use_bulk_app_name_logging (bool): Whether bulk logging to the application name file is enabled.
    td_api_debug (bool): Whether TD API debugging is enabled.

    Instance Attributes:
    _log_name (str): The name of the log file.
    _log (Logger): An instance of the logging.Logger class for logging messages.

    Methods:
    __init__(self, log_name: str) -> None: Initializes a TdLogger object for logging messages to the console and a file (if config present).

    Notes:
        All instance methods will log to both the class logger and instance logger.
    """

    _config = TdConfiguration()
    app_name = _config.app_info.app_name

    # Potentially does bulk logging to app_name file
    #  Always logs to console
    class_logger = logging.getLogger(app_name)

    config_present = _config.logging.config_present
    log_root_path = _config.logging.log_root_path if config_present else None
    use_bulk_app_name_logging = (
        _config.logging.use_bulk_app_name_logging if config_present else False
    )
    td_api_debug = False

    if "TD_API_DEBUG" in environ:
        debug_env_var_lower = getenv("TD_API_DEBUG").lower()
        if (
            debug_env_var_lower == "true"
            or debug_env_var_lower == "yes"
            or debug_env_var_lower == "1"
        ):
            td_api_debug = True
        else:
            td_api_debug = False
        if td_api_debug:
            class_logger.setLevel(logging.DEBUG)
    else:
        class_logger.setLevel(logging.INFO)

    _log_handler_file = None
    # Add file logger if config has logging section and useclass_loggerger True
    if config_present:
        if use_bulk_app_name_logging:
            _log_handler_file = initialize_file_log(
                app_name, log_root_path, td_api_debug
            )

    # Always log in the console
    _log_handler_console = logging.StreamHandler()

    if td_api_debug:
        _log_handler_console.setLevel(logging.DEBUG)
    else:
        _log_handler_console.setLevel(logging.INFO)

    _log_handler_console.setFormatter(colored_log_formatter)

    if len(class_logger.handlers) == 0:
        class_logger.addHandler(_log_handler_console)
        if _log_handler_file is not None:
            class_logger.addHandler(_log_handler_file)

    def __init__(self, log_name: str) -> None:
        """
        Initializes a TdLogger object for logging messages to the console and a file.

        Parameters:
        log_name (str): The name of the log file.
        """

        if not TdLogger.config_present:
            self.logger = TdLogger.class_logger
            return

        if log_name is None:
            log_name = "unknown-module"

        self.logger_name = f"{TdLogger.app_name}.{log_name}"
        self.logger = logging.getLogger(self.logger_name)

        if TdLogger.td_api_debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        if len(self.logger.handlers) == 0:
            self.logger.addHandler(
                initialize_file_log(
                    log_name, TdLogger.log_root_path, TdLogger.td_api_debug
                )
            )
