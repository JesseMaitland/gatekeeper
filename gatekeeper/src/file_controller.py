from hashlib import sha1
from typing import Tuple
from pathlib import Path


class FileController:

    def __init__(self, path: Path) -> None:
        self.path = path

    def get_file(self, name: str) -> Path:
        for path in self.path.iterdir():
            if path.is_file() and name == path.name:
                return path
        else:
            raise FileNotFoundError

    def save_file(self, name: str, content: str) -> None:
        file = self.path / name
        file.touch(exist_ok=True)
        file.write_text(content)

    def delete_file(self, name: str) -> None:
        file = self.get_file(name)
        file.unlink()

    def delete_files(self) -> None:
        for path in self.path.iterdir():
            if path.is_file():
                path.unlink()

    def hash_file(self, name: str) -> Tuple[str]:
        path = self.get_file(name)
        digest = sha1(path.read_text().encode()).hexdigest()
        return digest, name
