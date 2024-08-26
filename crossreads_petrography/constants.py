import os
from pathlib import Path
import shutil
from typing import Any
import yaml
import re
from types import SimpleNamespace
import importlib.resources

try:
    from google.colab import auth, drive
    from google.auth import default

    IN_COLAB = True
except ImportError:
    IN_COLAB = False


PATH_HERE = Path(__file__).parent.resolve()
PATH_REPO = PATH_HERE.parent.resolve()
PATH_REPO_DATA = PATH_REPO / "data"
PATH_CONFIG_DEFAULT = PATH_REPO / "data" / "default_config.yaml"

PATH_HOME = Path.home() / "crossreads_petrography_data"
PATH_HOME.mkdir(exist_ok=True)
