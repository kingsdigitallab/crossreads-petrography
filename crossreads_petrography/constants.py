from pathlib import Path
CREDENTIALS_PATH = Path.home() / '.config' / 'crossreads_petrography' / 'credentials.json'
PATH_HERE = Path(__file__).parent.resolve()
PATH_REPO = PATH_HERE.parent.resolve()
PATH_DATA = PATH_REPO / 'data'
PATH_INPUT_DATA = PATH_DATA / 'input'
PATH_OUTPUT_DATA = PATH_DATA / 'output'

for path in [PATH_INPUT_DATA, PATH_OUTPUT_DATA]:
    path.mkdir(parents=True, exist_ok=True)

SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1QDZ6Fc3o95q6ylvkjoNDOFeqNz7Nub8qQCPVV62Pus8/edit'
