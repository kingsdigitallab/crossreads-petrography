from pathlib import Path
CREDENTIALS_PATH = Path.home() / '.config' / 'crossreads_petrography' / 'credentials.json'
PATH_HERE = Path(__file__).parent.resolve()
PATH_REPO = PATH_HERE.parent.resolve()
PATH_DATA = PATH_REPO / 'data'
PATH_INPUT_DATA = PATH_DATA / 'input'

