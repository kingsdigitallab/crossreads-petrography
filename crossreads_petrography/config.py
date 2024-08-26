from . import *
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
config_str = substitute_variables(
    config_str, config_dict
)  # Second pass for nested substitutions


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
        import json
        return json.dumps(self.to_dict(), indent=2)

    def __bool__(self):
        return bool(self.__dict__)

    @classmethod
    def from_dict(cls, dictionary):
        def convert(value):
            if isinstance(value, dict):
                return cls.from_dict(value)
            elif isinstance(value, list):
                return [convert(item) for item in value]
            if type(value) == str:
                if value.startswith("~/"):
                    value = os.path.expanduser(value)
                if value.startswith("/") and not "\n" in value:
                    value = Path(value)
            return value

        return cls(**{k: convert(v) for k, v in dictionary.items()})

    def get(self, key_path: str):
        if key_path.startswith("config."):
            key_path = key_path[len("config.") :]
        keys = key_path.split(".")
        value = self
        for key in keys:
            if isinstance(value, DotDict) and hasattr(value, key):
                value = getattr(value, key)
            else:
                return None
        return value

    def to_dict(self):
        return {
            k: (
                (
                    str(v)
                    if not (str(v).startswith("{") and str(v).endswith("}"))
                    else self.get(str(v)[1:-1])
                )
                if not isinstance(v, DotDict)
                else v.to_dict()
            )
            for k, v in self.__dict__.items()
        }

    def to_df(self, index_names = ['config_type', 'path_name', 'path_type']):
        import pandas as pd

        def flatten_dict(d, parent_key="", sep="."):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
            return dict(items)

        flat_dict = flatten_dict(self.to_dict())
        index = pd.MultiIndex.from_tuples([tuple(key.split(".") + [''] * 3)[:3] for key in flat_dict.keys()])
        return pd.DataFrame({"value": flat_dict.values()}, index=index).rename_axis(index_names).fillna('')
    
    def _repr_html(self):
        return self.to_df().to_html()


CONFIG = config = DotDict.from_dict(yaml.safe_load(config_str))  # second pass


# PATH_DATA = Path(config.paths.data.local)
# # PATH_INPUT_DATA = PATH_DATA / "input"
# # PATH_OUTPUT_DATA = PATH_DATA / "output"
# # for path in [PATH_INPUT_DATA, PATH_OUTPUT_DATA]:
# #     path.mkdir(parents=True, exist_ok=True)


# # Copy default config to user config if it doesn't exist
# if not PATH_CONFIG.exists():
#     shutil.copy(PATH_CONFIG_DEFAULT, PATH_CONFIG)
#     print(f"Created default config file at {PATH_CONFIG}")

# if not PATH_DATA.exists():
#     shutil.copytree(PATH_REPO_DATA, PATH_DATA)
#     print(f"Copied default data to {PATH_DATA}")
