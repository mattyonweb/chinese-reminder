import dataclasses
from pathlib import Path
from platformdirs import *
import json

# Important global variables
APPNAME = "chinese-remainder"
CONFIG_DIR  = Path(user_config_dir(APPNAME, version="V1"))
CONFIG_FILE = CONFIG_DIR / "config.json"

# Create configuration directory if it doesnt exists (first run)
if not CONFIG_DIR.exists():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


@dataclasses.dataclass
class Configuration:
    dictionary_fpath: Path

    def __init__(self, d: dict):
        """ Gets fed by a json load. """
        if "dictionary_fpath" in d:
            self.dictionary_fpath = Path(d["dictionary_fpath"])
        else:
            self.dictionary_fpath = CONFIG_DIR / "dictionary.tsv"


def read_config_file():
    """ Read config file if it exists, otherwise create an empty one """
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w") as f:
            f.write("{}")

    with open(CONFIG_FILE, "r") as f:
        return Configuration(json.load(f))


APP_CONFIG = read_config_file()
