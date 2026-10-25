"""Loading shared game data from the project's data directory."""

import json
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"


def load_json(filename: str) -> dict:
    """Load one JSON data file from the project's data directory."""
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)
