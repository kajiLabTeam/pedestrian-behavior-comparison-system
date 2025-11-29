from __future__ import annotations
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True, slots=True)
class LoggingContext:
    """Holds logging state and run-specific paths."""

    logger: logging.Logger
    run_dir: Path
    log_file: Path


def setup_logging() -> LoggingContext:
    """Configure logging and prepare a timestamped run directory."""

    base_path = Path("output")
    base_path.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = base_path / ts
    run_dir.mkdir(parents=True, exist_ok=True)

    log_file = run_dir / f"{ts}.log"

    logger = logging.getLogger("pedestrian")

    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logger.info(
        "Logging initialised.  level=%s run_dir=%s",
        logging.getLevelName(logger.level),
        run_dir,
    )

    return LoggingContext(
        logger=logger,
        run_dir=run_dir,
        log_file=log_file,
    )
