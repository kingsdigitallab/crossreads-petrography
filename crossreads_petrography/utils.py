from .imports import *

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

def get_crossreads_spreadsheet():
    return get_spreadsheet(SPREADSHEET_URL)

# @cache
def read_crossreads_spreadsheet(worksheet_index=0):
    return read_spreadsheet(SPREADSHEET_URL, worksheet_index=worksheet_index)


def get_spreadsheet(spreadsheet_url, credentials_path: Optional[str] = None):
    """
    Authenticate and access Google Spreadsheet using Colab auth if available,
    otherwise use gspread with service account credentials.
    """
    logger.debug("Authenticating and accessing Google Spreadsheet")
    
    if IN_COLAB:
        if auth is None:
            raise ImportError("Failed to import google.colab.auth")
        auth.authenticate_user()
        creds, _ = default()
    else:
        creds_path = credentials_path or CREDENTIALS_PATH
        if os.path.exists(creds_path):
            creds = service_account.Credentials.from_service_account_file(
                creds_path,
                scopes=["https://www.googleapis.com/auth/spreadsheets"],
            )
        else:
            raise FileNotFoundError(f"Credentials file not found: {creds_path}")

    gc = gspread.authorize(creds)
    return gc.open_by_url(spreadsheet_url)

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

    df = df.set_index(first_column)
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

def read_df(filename: str) -> pd.DataFrame:
    """
    Read a dataframe from various file formats (csv, xlsx, xls, tsv).
    
    Args:
        filename (str): Path to the file.
    
    Returns:
        pd.DataFrame: The loaded dataframe.
    """
    logger.debug(f"Reading dataframe from file: {filename}")
    
    file_extension = os.path.splitext(filename.lower())[1]
    
    try:
        if file_extension == '.csv':
            # Detect separator for CSV files
            with open(filename, 'r') as f:
                sample = f.read(4096)  # Read more of the file
                try:
                    dialect = csv.Sniffer().sniff(sample)
                    separator = dialect.delimiter
                except csv.Error:
                    # Fallback to common separators if sniffing fails
                    for sep in [',', ';', '\t', '|']:
                        if sep in sample:
                            separator = sep
                            break
                    else:
                        separator = ','  # Default to comma if nothing else works
            
            return pd.read_csv(filename, sep=separator)
        elif file_extension in ['.xlsx', '.xls']:
            return pd.read_excel(filename)
        elif file_extension == '.tsv':
            return pd.read_csv(filename, sep='\t')
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    except Exception as e:
        logger.error(f"Error reading file {filename}: {str(e)}")
        raise
    
def read_input_data_folder(folder: str) -> pd.DataFrame:
    """
    Read XRD input data from a folder, either on Google Drive or local path.
    """
    logger.debug(f"Reading spreadsheet data from {folder}")

    if IN_COLAB:
        if drive is None:
            raise ImportError("Failed to import google.colab.drive")
        drive.mount('/content/drive')
        folder = os.path.join('/content/drive/MyDrive', folder)

    df = pd.concat(
        read_df(os.path.join(folder, ifn))
        for ifn in os.listdir(folder)
        if os.path.splitext(ifn)[-1].lower() in {".csv",".tsv",".xls",".xlsx"}
    ).fillna("")

    logger.debug(f"Read {len(df)} rows from input data")
    return df

def read_input_data_folder_txt(folder:str) -> str:
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
    for ifn in os.listdir(folder):
        if ifn.endswith('.txt'):
            with open(os.path.join(folder,ifn)) as f:
                o.append(f.read())
    
    return '\n\n\n\n'.join(o)



def show_img(path):
    try:
        from IPython.display import Image, display
        display(Image(filename=path))
    except Exception:
        pass
