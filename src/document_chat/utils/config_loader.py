import os
from pathlib import Path
import yaml

def _project_load() -> Path:
    return Path(__file__).resolve().parents[3]

def load_config(config_path:str):
    env_path=os.getenv("config_path")
    if config_path is None:
        config_path=env_path

    path=Path(config_path)
    if not path.is_absolute():
        path=_project_load()/path

    if not path.exists():
        raise FileNotFoundError("config file not found")

    with open(path,"r") as f:
        return yaml.safeload(f) as {}


