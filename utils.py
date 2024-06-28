# coding: utf8
import json
from pathlib import Path


def read_template(browser: str) -> dict:
    filepath = Path(__file__).parent / "templates" / f"{browser}.json"
    if not filepath.exists():
        return {}
    return json.loads(filepath.read_text("utf8"))
