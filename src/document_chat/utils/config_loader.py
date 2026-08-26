import os
from pathlib import Path
import yaml

def _project_load() -> Path:
    return Path(__file__).resolve().parents[2]

def load_config(config_path:str=None):

    if config_path is None:
        config_path=os.getenv("config_path")

    if not config_path:
        raise ValueError(
            "CONFIG_PATH environment variable is not set"
        )

    path=Path(config_path)
    print(path)
    if not path.is_absolute():
        path=_project_load()/path

    if not path.exists():
        raise FileNotFoundError("config file not found :{path}")

    with open(path,"r") as f:
        return yaml.safe_load(f) or {}


