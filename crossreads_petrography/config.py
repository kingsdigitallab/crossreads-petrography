from functools import cached_property
import logging
from collections import UserDict
import yaml
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config(UserDict):
    def __init__(self, yaml_path):
        super().__init__()
        self.yaml_path = Path(yaml_path)
        logger.info(f"Initializing Config with yaml_path: {self.yaml_path}")
        self.load_config()

    def load_config(self):
        logger.info(f"Loading config from {self.yaml_path}")
        with open(self.yaml_path, "r") as f:
            config = yaml.safe_load(f)
        data = self.flatten_dict(config)
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = os.path.expanduser(v)
                logger.debug(f"Expanded user path for key {k}: {data[k]}")

        def convert(v1):
            was_posix = isinstance(v1, Path)
            v = str(v1)
            # Get list of matched groups of text between { and }
            while ("{" in v) and ("}" in v):
                placeholders = [
                    x.split("}")[0].strip() for x in v.split("{")[1:] if "}" in x
                ]
                for placeholder in placeholders:
                    expanded_value = data.get(placeholder, "")
                    v = v.replace("{" + placeholder + "}", str(expanded_value))
                    logger.debug(f"Replaced placeholder {placeholder} with {expanded_value}")
            v = Path(v) if was_posix else v
            return v

        self.data = {k: convert(v) for k, v in data.items()}
        logger.info("Config loaded and processed successfully")

    def flatten_dict(self, d, parent_key=""):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)

    @property
    def df(self):
        import pandas as pd

        return pd.DataFrame(list(self.items()), columns=["key", "value"]).set_index(
            "key"
        )

    def get(self, key, default=None):
        from .constants import IN_COLAB

        res = self.data.get(key, None)
        if res is not None:
            logger.debug(f"Found value for key {key}: {res}")
            return res

        if IN_COLAB and key + ".colab" in self.data:
            colab_value = self.data[key + ".colab"]
            logger.info(f"Using Colab-specific value for key {key}: {colab_value}")
            return colab_value

        for suffix in [".url.prod", ".url.dev", ".url", ".local"]:
            res = self.data.get(key + suffix)
            if res is not None:
                logger.info(f"Found value for key {key} with suffix {suffix}: {res}")
                return res

        logger.warning(f"Key {key} not found in config, returning default: {default}")
        return default

    def __getitem__(self, key):
        res = self.get(key)
        if res is None:
            logger.error(f"Key {key} not found in config")
            raise KeyError(f"Key {key} not found in config")
        return res

    @cached_property
    def paths(self):
        path_keys = {
            k.split('.local')[0].split('.colab')[0].split('.url')[0]
            for k in self.data.keys()
            if k.endswith(".local")
            or k.endswith(".colab")
            or k.endswith(".url.prod")
            or k.endswith(".url.dev")
            or k.endswith(".url")
        }
        return {'.'.join(k.split('.')[1:]): self.get(k,'') for k in path_keys}


PATH_CONFIG = Path.home() / "crossreads_petrography_data" / "config.yaml"
PATH_CONFIG_DEFAULT = Path(__file__).parent / "config.yaml"

if PATH_CONFIG.exists():
    logger.info(f"Using user-specific config file: {PATH_CONFIG}")
    config = Config(PATH_CONFIG)
else:
    logger.info(f"User-specific config not found. Using default config: {PATH_CONFIG_DEFAULT}")
    config = Config(PATH_CONFIG_DEFAULT)