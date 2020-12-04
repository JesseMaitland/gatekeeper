

def format_model_name(name: str) -> str:
    return name.rstrip('s').capitalize()


def format_template_name(name: str) -> str:
    return f"{name.rstrip('s').lower()}.sql"


def format_render_key(name: str) -> str:
    return name.rstrip('s').lower()
