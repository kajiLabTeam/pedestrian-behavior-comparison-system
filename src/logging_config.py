from __future__ import annotations
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True, slots=True)
class LoggingContext:
    """ログ用の状態と実行時の出力パスを保持するデータクラス。

    このクラスは、ログ出力を行う際に必要となるロガー本体と、
    当該実行で生成される出力物（ログファイルやCSV/画像）を格納する
    実行専用ディレクトリのパスをまとめて渡すために使います。

    English:
        Holds logging state and run-specific paths.

    Attributes
    ----------
    logger:
        `logging.Logger` オブジェクト。アプリケーション全体で使うロガー。これを使ってログ出力を行います。
    run_dir:
        実行ごとに生成される出力ディレクトリの `Path`（例: `output/20251129_123456`）。
        ログ・生成CSV・画像をここに保存します。
    input_trjcsv_dir:
                入力の軌跡CSVファイルが格納されているディレクトリの `Path` (例: `input/demo/`)。
    """

    logger: logging.Logger
    run_dir: Path
    input_trjcsv_dir: Path


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
        "Loggingを初期化しました。 level=%s run_dir=%s",
        logging.getLevelName(logger.level),
        run_dir,
    )

    return LoggingContext(
        logger=logger,
        run_dir=run_dir,
        input_trjcsv_dir=Path("input/demo"),
    )
