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
PATH_REPO_DATA = PATH_REPO / 'data'
PATH_CONFIG_DEFAULT = PATH_REPO / "data" / "default_config.yaml"

PATH_HOME = Path.home() / "crossreads_petrography_data"
PATH_HOME.mkdir(exist_ok=True)
PATH_CONFIG = PATH_HOME / "config.yaml"




# Load configuration from user config.yaml
config_path = PATH_CONFIG if PATH_CONFIG.exists() else PATH_CONFIG_DEFAULT
with open(config_path, "r") as config_file:
    config_str = config_file.read()

# Custom variable substitution
def substitute_variables(config_str, config_dict):
    def get_value(keys):
        value = config_dict
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value

    def replace(match):
        keys = match.group(1).split(".")
        value = get_value(keys)
        if value is None:
            return match.group(0)  # Return original if key not found
        return str(value)

    pattern = r"\{([^}]+)\}"
    prev_config_str = ""
    while prev_config_str != config_str:
        prev_config_str = config_str
        config_str = re.sub(pattern, replace, config_str)
    
    return config_str


# Perform substitution and load YAML
config_str = substitute_variables(config_str, yaml.safe_load(config_str))
config_dict = yaml.safe_load(config_str)
config_str = substitute_variables(config_str, config_dict)  # Second pass for nested substitutions

class DotDict(SimpleNamespace):
    def __getitem__(self, key):
        return getattr(self, key, DotDict())

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            return DotDict()
        
    def __repr__(self):
        return json.dumps({k: v if not isinstance(v, DotDict) else v.__dict__ for k, v in self.__dict__.items()}, indent=2)
    
    def __bool__(self):
        return bool(self.__dict__)

    @classmethod
    def from_dict(cls, dictionary):
        def convert(value):
            if isinstance(value, dict):
                return cls.from_dict(value)
            elif isinstance(value, list):
                return [convert(item) for item in value]
            if type(value)==str:
                if value.startswith('~/'):
                    value = os.path.expanduser(value)
                if value.startswith('/') and not '\n' in value:
                    value = Path(value)
            return value

        return cls(**{k: convert(v) for k, v in dictionary.items()})


CONFIG = config = DotDict.from_dict(yaml.safe_load(config_str)) # second pass





PATH_DATA = config.paths.data.local
# PATH_INPUT_DATA = PATH_DATA / "input"
# PATH_OUTPUT_DATA = PATH_DATA / "output"
# for path in [PATH_INPUT_DATA, PATH_OUTPUT_DATA]:
#     path.mkdir(parents=True, exist_ok=True)



# Copy default config to user config if it doesn't exist
if not PATH_CONFIG.exists():
    shutil.copy(PATH_CONFIG_DEFAULT, PATH_CONFIG)
    print(f"Created default config file at {PATH_CONFIG}")

if not PATH_DATA.exists():
    shutil.copytree(PATH_REPO_DATA, PATH_DATA)
    print(f"Copied default data to {PATH_DATA}")