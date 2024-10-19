import logging
from pathlib import Path
import os


def setup_logging():
    logger = logging.getLogger("TimeTracker")
    logger.setLevel(logging.INFO)

    app_data = Path(os.getenv("LOCALAPPDATA", str(Path.home())))
    log_dir = app_data / "TimeTracker" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    fh = logging.FileHandler(log_dir / "timetracker.log")
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
