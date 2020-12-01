from pathlib import Path


class Queries:

    def __init__(self):
        self.query_path = Path(__file__).parent / "queries"

    def get_query(self, name: str) -> str:
        path = self.query_path / f"{name}.sql"
        return path.read_text()
