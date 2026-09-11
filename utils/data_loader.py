"""
Загрузка данных из файлов
"""
import csv
import logging
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_data(filename: str) -> List[Dict[str, str]]:
    with open(DATA_DIR / filename, newline = "", encoding = "utf_8_sig") as f:
        reader = csv.DictReader(f)
        return [
            {
                k.strip(): (v.strip() if v else "")
                for k, v in d.items()
            }
            for d in reader
        ]