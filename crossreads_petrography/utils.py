from . import *


# Add these lines at the top of the file
auth = None
drive = None
default = None

if in_colab():
    try:
        from google.colab import auth, drive
        from google.auth import default
    except ImportError:
        pass

def get_crossreads_spreadsheet(key='petrography'):
    url_or_path=get_path(key)
    if type(url_or_path) == str and url_or_path.startswith('http'):
        return get_spreadsheet(url_or_path)
    

def read_metadata(metamorphic=True):
    df = read_path('metadata.metamorphic' if metamorphic else 'metadata.sedimentary')
    df=df.set_index(df.columns[0])
    return df

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

    if in_colab():
        if drive is None:
            raise ImportError("Failed to import google.colab.drive")
        if not os.path.exists('/content/drive/MyDrive'):
            drive.mount('/content/drive')
        folder = os.path.join('/content/drive/MyDrive', folder)

    l = [
        read_df(os.path.join(folder, ifn), sep=sep)
        for ifn in os.listdir(folder)
        if os.path.splitext(ifn)[-1].lower() in {".csv",".tsv",".xls",".xlsx"} and not ifn.startswith('.') and not ifn.startswith('~$')
    ]
    df=pd.concat(l).fillna("") if l else pd.DataFrame()

    logger.debug(f"Read {len(df)} rows from input data")
    return df

def read_input_data_folder_txt(folder:str, as_list=False) -> str:
    """
    Read XRD input data from a folder, either on Google Drive or local path.
    """
    logger.debug(f"Reading txt data from {folder}")

    if in_colab():
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






def get_path(paths):
    if is_pathlike(paths): return Path(paths)
    return Path(config.get_path(paths))

def is_urllike(x):
    """
    Check if the given string is a URL-like string.
    """
    if isinstance(x, str):
        return x.startswith('http://') or x.startswith('https://')
    return False

def is_pathlike(x):
    return isinstance(x, (str, Path)) and (os.path.isabs(x) or Path(x).exists())


def read_path(path, worksheet_index=0, as_list=False, sep=','):
    from .config import config
    path = get_path(path)
    assert is_pathlike(path)
    if path.is_dir():
        logger.debug(f"Path is a directory: {path}")
        txt_files = list(path.glob('*.txt'))
        if txt_files and all(f.suffix == '.txt' or f.name.startswith('.') for f in path.iterdir()):
            logger.debug(f"Directory contains only .txt files: {path}")
            return read_input_data_folder_txt(str(path), as_list=as_list)
        else:
            logger.debug(f"Directory contains non-txt files: {path}")
            return read_input_data_folder(str(path), sep=sep)
    
    else:
        logger.debug(f"Path is a file: {path}", path.suffix.lower())
        if path.suffix.lower() in ['.csv', '.xlsx', '.xls', '.tsv']:
            logger.debug(f"File is a spreadsheet: {path}")
            res = read_df(str(path), sep=sep)
            logger.debug(f"Read {len(res)} rows from spreadsheet")
            logger.debug(res)
            return res
        else:
            logger.debug(f"File is not a recognized spreadsheet format: {path}")
            try:
                return path.read_text()
            except Exception as e:
                logger.error(f"Error reading file {path}: {str(e)}")
                return None