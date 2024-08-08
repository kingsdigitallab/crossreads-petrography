from .imports import *
from gspread.exceptions import APIError
from pathlib import Path


# Add these lines at the top of the file
auth = None
drive = None
default = None

if IN_COLAB:
    try:
        from google.colab import auth, drive
        from google.auth import default
    except ImportError:
        pass

def get_crossreads_spreadsheet(key='petrography'):
    url_or_path=get_path(key)
    if type(url_or_path) == str and url_or_path.startswith('http'):
        return get_spreadsheet(url_or_path)
    

@cache
def read_crossreads_spreadsheet(worksheet_index=0):
    df=read_path('petrography', worksheet_index=worksheet_index)
    df=df.set_index(df.columns[0])
    return df


def authenticate_colab():
    """
    Authenticate using Google Colab's auth.
    """
    if auth is None:
        raise ImportError("Failed to import google.colab.auth")
    auth.authenticate_user()
    creds, _ = default()
    return creds

def authenticate_service_account(credentials_path: str):
    """
    Authenticate using a service account file.
    """
    return service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )

def get_spreadsheet(spreadsheet_url, credentials_path: Optional[str] = None):
    """
    Authenticate and access Google Spreadsheet using Colab auth if available,
    otherwise use gspread with service account credentials.
    """
    logger.debug("Authenticating and accessing Google Spreadsheet")
    
    if not has_credentials():
        raise ValueError("No credentials available. Unable to access spreadsheet.")
    
    creds = None
    if IN_COLAB:
        creds = authenticate_colab()
    else:
        creds_path = credentials_path or config.paths.credentials.local
        if not Path(creds_path).exists():
            raise FileNotFoundError(f"Credentials file not found: {creds_path}")
        creds = authenticate_service_account(creds_path)
    
    if creds:
        try:
            gc = gspread.authorize(creds)
            return gc.open_by_url(spreadsheet_url)
        except Exception as e:
            logger.error(f"Error accessing spreadsheet: {e}")
            raise
    
    raise ValueError("Unable to authenticate and access spreadsheet.")

def read_spreadsheet(spreadsheet: 'Spreadsheet|str', worksheet_index: int = 0) -> pd.DataFrame:
    """
    Read data from a Google Spreadsheet worksheet and return as a DataFrame.
    """
    if type(spreadsheet)==str:
        spreadsheet=get_spreadsheet(spreadsheet)
    logger.debug(f"Reading data from spreadsheet worksheet {worksheet_index}")
    worksheet = spreadsheet.get_worksheet(worksheet_index)
    rows = worksheet.get_all_values()
    df = pd.DataFrame.from_records(rows)
    df.columns = list(df.iloc[0])
    df = df.drop(0)

    # Remove rows with empty or NaN values in the first column
    first_column = df.columns[0]
    df = df.dropna(subset=[first_column])
    df = df[df[first_column] != ""]

    # df = df.set_index(first_column)
    logger.debug(f"Read {len(df)} rows from spreadsheet")
    return df

def update_spreadsheet(spreadsheet: gspread.Spreadsheet, df: pd.DataFrame, worksheet_index: int = 0):
    """
    Update a Google Spreadsheet worksheet with data from a DataFrame.
    """
    logger.debug(f"Updating Google Sheet with processed data ({len(df)} rows)")
    df = df.reset_index()
    worksheet = spreadsheet.get_worksheet(worksheet_index)
    data_to_update = [df.columns.values.tolist()] + df.values.tolist()
    logger.debug(
        f"Preparing to update {len(data_to_update)} rows and {len(data_to_update[0])} columns"
    )
    res = worksheet.update(data_to_update)
    if not isinstance(res, dict) or not (res.get("spreadsheetId") and res.get("updatedCells")):
        logger.warning("Error updating Google Sheets worksheet")
    else:
        logger.debug(
            f"Successfully updated {res['updatedCells']} cells in the Google Sheets worksheet."
        )

def read_df(filename: str, sep=',') -> pd.DataFrame:
    """
    Read a dataframe from various file formats (csv, xlsx, xls, tsv).
    
    Args:
        filename (str): Path to the file.
    
    Returns:
        pd.DataFrame: The loaded dataframe.
    """
    filename=Path(filename)
    logger.debug(f"Reading dataframe from file: {filename.name}")
    
    file_extension = filename.suffix.lower()
    
    try:
        if file_extension == '.csv':
            # Detect separator for CSV files
            if not sep:
                with open(filename, 'r') as f:
                    sample = f.read(4096)  # Read more of the file
                    dialect = csv.Sniffer().sniff(sample)
                    separator = dialect.delimiter
                    print(f'{filename} has a separator character of {separator}')
            else:
                separator = sep
            
            odf = pd.read_csv(filename, sep=separator)
        elif file_extension in ['.xlsx', '.xls']:
            odf = pd.read_excel(filename)
        elif file_extension == '.tsv':
            odf = pd.read_csv(filename, sep='\t')
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    except Exception as e:
        logger.error(f"Error reading file {filename}: {str(e)}")
        raise

    return odf
    
def read_input_data_folder(folder: str, sep=',') -> pd.DataFrame:
    """
    Read XRD input data from a folder, either on Google Drive or local path.
    """
    logger.debug(f"Reading spreadsheet data from {os.path.basename(folder)}")

    if IN_COLAB:
        if drive is None:
            raise ImportError("Failed to import google.colab.drive")
        drive.mount('/content/drive')
        folder = os.path.join('/content/drive/MyDrive', folder)

    df = pd.concat(
        read_df(os.path.join(folder, ifn), sep=sep)
        for ifn in os.listdir(folder)
        if os.path.splitext(ifn)[-1].lower() in {".csv",".tsv",".xls",".xlsx"}
    ).fillna("")

    logger.debug(f"Read {len(df)} rows from input data")
    return df

def read_input_data_folder_txt(folder:str, as_list=False) -> str:
    """
    Read XRD input data from a folder, either on Google Drive or local path.
    """
    logger.debug(f"Reading txt data from {folder}")

    if IN_COLAB:
        if drive is None:
            raise ImportError("Failed to import google.colab.drive")
        drive.mount('/content/drive')
        folder = os.path.join('/content/drive/MyDrive', folder)

    o=[]
    fns=[]
    for ifn in os.listdir(folder):
        if ifn.endswith('.txt'):
            fns.append(ifn)
            with open(os.path.join(folder,ifn)) as f:
                o.append(f.read())
    
    return '\n\n\n\n'.join(o) if not as_list else list(zip(fns,o))



def show_img(path):
    try:
        from IPython.display import Image, display
        display(Image(filename=path))
    except Exception:
        pass





def has_credentials():
    return IN_COLAB or Path(config.paths.credentials.local).exists()

def get_path(paths):
    if isinstance(paths, str):
        if not paths.startswith('config.') and not paths.startswith('paths.'):
            paths = 'paths.' + paths
        paths = get_config_value(paths)

    if IN_COLAB:
        return Path(paths.colab) if paths.colab else Path(paths.local)
    
    if paths.url and has_credentials():
        if isinstance(paths.url, str):
            return paths.url
        if config.production and paths.url.prod:
            return paths.url.prod
        if paths.url.dev:
            return paths.url.dev

    return Path(paths.local) if paths.local else None    

def is_urllike(x):
    """
    Check if the given string is a URL-like string.
    """
    if isinstance(x, str):
        return x.startswith('http://') or x.startswith('https://')
    return False

def is_pathlike(x):
    return isinstance(x, (str, Path)) and (str(x).startswith('/') or Path(x).exists())


def read_path(paths, worksheet_index=0, as_list=False, sep=','):
    path = get_path(paths) if not is_pathlike(paths) and not is_urllike(paths) else paths
    
    if is_urllike(path):
        return read_spreadsheet(path, worksheet_index=worksheet_index)
    
    if is_pathlike(path):
        path = Path(path)
        if path.is_dir():
            txt_files = list(path.glob('*.txt'))
            if txt_files and all(f.suffix == '.txt' or f.name.startswith('.') for f in path.iterdir()):
                return read_input_data_folder_txt(str(path), as_list=as_list)
            else:
                return read_input_data_folder(str(path), sep=sep)
        
        if path.is_file():
            if path.suffix.lower() in ['.csv', '.xlsx', '.xls', '.tsv']:
                return read_df(str(path), sep=sep)
            else:
                try:
                    return path.read_text()
                except Exception as e:
                    logger.error(f"Error reading file {path}: {str(e)}")
                    return None
    
    return pd.DataFrame()

def get_config_value(key_path: str):
    if key_path.startswith('config.'): key_path=key_path[len('config.'):]
    keys = key_path.split('.')
    value = config
    for key in keys:
        if isinstance(value, DotDict) and hasattr(value, key):
            value = getattr(value, key)
        else:
            return None
    return value

