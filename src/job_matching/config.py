
"""Настройки приложения и логирования."""

import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLES_DIR = DATA_DIR / "samples"

CAP_PVL_VACANCIES = RAW_DATA_DIR / "cap_pvl" / "vacancies.csv"
HIMALAYAS_DATA_DIR = RAW_DATA_DIR / "himalayas"


def setup_logging(level: int = logging.INFO) -> None:
    """Настроить логирование приложения."""
    logging.basicConfig(
        level=level,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )
