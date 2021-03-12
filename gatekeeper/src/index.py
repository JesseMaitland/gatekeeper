import json
from typing import Dict
from hashlib import md5
from pathlib import Path


def read_index(path: Path) -> Dict[str, str]:
    try:
        content = path.read_text()
    except FileNotFoundError:
        return {}
    else:
        return json.loads(content)


def hash_file(content: str) -> str:
    return md5(content.encode()).hexdigest()


def save_index(path: Path, index: Dict[str, str]) -> None:
    json.dump(index, path.open(mode='w+'), indent=1)
