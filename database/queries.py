from pathlib import Path


class SqlManager:

    def __init__(self):
        self.root = Path(__file__).parent / "sql"

    def get_query(self, name: str) -> str:
        path = self.root / "queries" / f"{name}.sql"
        return path.read_text()

    def get_ddl(self, name: str) -> str:
        path = self.root / "ddl" / f"{name}.sql"
        return path.read_text()
