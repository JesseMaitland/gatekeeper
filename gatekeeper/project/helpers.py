from typing import List, Any


def format_model_name(name: str) -> str:
    return name.rstrip('s').capitalize()


def format_template_name(name: str) -> str:
    return f"{name.rstrip('s').lower()}.sql"


def format_render_key(name: str) -> str:
    return name.rstrip('s').lower()


def create_key_list(objs: List[Any], key: str) -> List[str]:
    return [getattr(x, key) for x in objs]
