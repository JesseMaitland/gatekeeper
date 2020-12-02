from pathlib import Path

QUERY_PATH = Path(__file__).parent / "sql" / "queries"


def get_query(name: str) -> str:
    path = QUERY_PATH / f"{name}.sql"
    return path.read_text()
