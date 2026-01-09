import yaml
from pathlib import Path
from functools import lru_cache

BASE_DIR = Path(__file__).resolve().parents[2]

CONFIG_DIR = BASE_DIR / "config"


def _load_yaml(filename: str) -> dict:
    path = CONFIG_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r") as f:
        return yaml.safe_load(f)


@lru_cache
def load_app_config() -> dict:
    """
    Infrastructure & resource config
    """
    return _load_yaml("app.yaml")


@lru_cache
def load_llm_config() -> dict:
    """
    LLM + retrieval behavior config
    """
    return _load_yaml("llm.yaml")

@lru_cache
def load_prompts() -> dict:
    path = Path("config/prompt.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)