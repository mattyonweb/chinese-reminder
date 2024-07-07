import dataclasses
from pathlib import Path
from platformdirs import user_config_dir
import json
import shutil

# Important global variables
APPNAME = "chinese-remainder"
CONFIG_DIR  = Path(user_config_dir(APPNAME, version="V1"))
CONFIG_FILE = CONFIG_DIR / "config.json"

# Create configuration directory if it doesnt exists (first run)
IS_FIRST_EXECUTION = not CONFIG_DIR.exists()
if IS_FIRST_EXECUTION:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


@dataclasses.dataclass
class Configuration:
    dictionary_fpath: Path
    sentences_fpath: Path
    verbose: bool

    def __init__(self, d: dict, first_execution: bool):
        """ Gets fed by a json load. """
        if first_execution:
            shutil.copy(r"examples/dictionary.tsv", CONFIG_DIR / "dictionary.tsv")
            shutil.copy(r"examples/sentences.tsv", CONFIG_DIR / "sentences.tsv")

        if "dictionary_fpath" in d:
            self.dictionary_fpath = Path(d["dictionary_fpath"])
        else:
            self.dictionary_fpath = CONFIG_DIR / "dictionary.tsv"

        # italian - chinese sentences database
        if "sentences_fpath" in d:
            self.sentences_fpath = Path(d["sentences_fpath"])
        else:
            self.sentences_fpath = CONFIG_DIR / "sentences.tsv"

        # debug informatoins
        if "verbose" in d:
            self.verbose = d["verbose"].lower().strip() == "true"
        else:
            self.verbose = False


def read_config_file():
    """ Read config file if it exists, otherwise create an empty one """
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w") as f:
            f.write("{}")

    with open(CONFIG_FILE, "r") as f:
        return Configuration(json.load(f), IS_FIRST_EXECUTION)


APP_CONFIG = read_config_file()
