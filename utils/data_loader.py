"""
Загрузка данных из файлов
"""
import csv
import xml.etree.ElementTree as ET
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def _convert_value(value: str) -> Any:

    if value is None:
        return ""

    try:
        return float(value)
    except ValueError:
        pass

    try:
        return int(value)
    except ValueError:
        pass

    return value

def load_data_csv(filename: str) -> Dict[str, List[Dict[str, Any]]]:
    filepath = DATA_DIR / filename
    logger.debug("Загружаю CSV-файл: %s", filepath)

    with open(filepath, newline="", encoding="utf_8_sig") as f:
        reader = csv.DictReader(f)
        rows = [
            {
                k.strip(): _convert_value(v)
                for k, v in d.items()
            }
            for d in reader
        ]

    result: Dict[str, List[Dict[str, Any]]] = {"positive": [], "negative": []}
    for row in rows:
        case_type = str(row.pop("type", "positive"))
        result[case_type].append(row)

    logger.info("CSV-файл загружен: %s, positive: %d, negative: %d",
                filepath, len(result["positive"]), len(result["negative"]))
    return result

def load_data_xml(filename: str) -> Dict[str, List[Dict[str, Any]]]:
    filepath = DATA_DIR / filename

    logger.debug("Загружаю XML-файл: %s", filepath)

    tree = ET.parse(filepath)
    root = tree.getroot()

    result: Dict[str, List[Dict[str, Any]]] = {"positive": [], "negative": []}

    for cases in root.findall("cases"):
        case_type: str = cases.get("type") or "positive"
        for case in cases.findall("case"):
            item: Dict[str, Any] = {}
            for child in case:
                item[child.tag] = _convert_value(child.text or "")
            result[case_type].append(item)

    logger.info("XML-файл загружен: %s, positive: %d, negative: %d",
                filepath, len(result["positive"]), len(result["negative"]))
    return result