from . import *

def in_colab():
    try:
        from google.colab import auth, drive
        from google.auth import default
        return True
    except ImportError:
        return False


PATH_HERE = Path(__file__).parent.resolve()
PATH_REPO = PATH_HERE.parent.resolve()
PATH_REPO_DATA = PATH_REPO / "data"
PATH_CONFIG_DEFAULT = PATH_REPO / "data" / "default_config.yaml"

PATH_HOME = Path.home() / "crossreads_petrography_data"
PATH_HOME.mkdir(exist_ok=True)
