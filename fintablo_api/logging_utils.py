"""Logging configuration helpers for the FinTablo API client."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    log_level: str = "INFO",
    log_to_file: bool = False,
    log_file_path: str = "logs/fintablo.log",
) -> logging.Logger:
    """
    Configure root logging for applications that consume this package.

    The client defaults to console logging only. Enabling `log_to_file`
    will append to ``log_file_path`` and create intermediate directories
    if necessary.
    """

    parsed_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create logs directory if we need to write to file.
    if log_to_file:
        Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    root_logger = logging.getLogger()

    # Remove any previously configured handlers to avoid duplication.
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(parsed_level)
    console_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(console_handler)
    root_logger.setLevel(parsed_level)

    if log_to_file:
        file_handler = logging.FileHandler(log_file_path, mode="a")
        file_handler.setLevel(parsed_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        root_logger.addHandler(file_handler)

    # Keep noisy dependencies quiet unless explicitly reconfigured.
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)

    # Ensure package namespace stays verbose for troubleshooting.
    package_logger = logging.getLogger("fintablo_api")
    package_logger.setLevel(logging.DEBUG)
    package_logger.propagate = True

    return package_logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Retrieve a namespaced logger within the fintablo_api hierarchy.

    Examples:
        get_logger() -> 'fintablo_api'
        get_logger("http_client") -> 'fintablo_api.http_client'
    """

    qualified_name = "fintablo_api"
    if name:
        qualified_name = f"{qualified_name}.{name}"

    logger = logging.getLogger(qualified_name)
    logger.propagate = True
    return logger
