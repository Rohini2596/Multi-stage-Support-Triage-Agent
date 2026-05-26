from pathlib import Path
from datetime import datetime
LOG_DIR = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "logs"
)
LOG_DIR.mkdir(
    exist_ok=True
)
LOG_FILE = (
    LOG_DIR / "log.txt"
)
class PipelineLogger:
    def __init__(self):
        self.log_file = LOG_FILE
    def log(
        self,
        message: str
    ):
        timestamp = (
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
        final = (
            f"[{timestamp}] "
            f"{message}\n"
        )
        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as f:
            f.write(final)