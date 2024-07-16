import os
import pandas as pd
import numpy as np
import gspread
from google.oauth2 import service_account
from .constants import *
from .utils import *
from loguru import logger
import sys
logger.remove()
logger.add(
    sink=sys.stderr,
    format="<level>{message}</level><cyan> @ {time:YYYY-MM-DD HH:mm:ss,SSS}</cyan>",
    level="DEBUG",
)
from functools import cache
from collections import defaultdict


class XRDConverter:
    def __init__(self, input_folder=None, credentials_path=None):
        self.input_folder = input_folder or PATH_XRD_INPUT_DATA
        self.credentials_path = credentials_path or CREDENTIALS_PATH
        logger.debug(f"Initializing XRDConverter with input folder: {self.input_folder}")
        self.spreadsheet = self.get_spreadsheet()

    def get_spreadsheet(self):
        logger.debug("Authenticating and accessing Google Spreadsheet")
        creds = None
        if os.path.exists(self.credentials_path):
            creds = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=["https://www.googleapis.com/auth/spreadsheets"],
            )
        else:
            raise FileNotFoundError(
                f"Credentials file not found: {self.credentials_path}"
            )

        gc = gspread.authorize(creds)
        return gc.open_by_url(SPREADSHEET_URL)

    @cache
    def read_xrd_data(self):
        logger.debug(f"Reading XRD data from {self.input_folder}")
        df = pd.concat(
            pd.read_csv(os.path.join(self.input_folder, ifn), sep=";")
            for ifn in os.listdir(self.input_folder)
            if os.path.splitext(ifn)[-1].lower() == ".csv"
        ).fillna("")
        paramcol = "Parameter, Goal"
        df = df[~df[paramcol].isin(COLS_TO_IGNORE)]
        
        data=defaultdict(dict)
        extra=defaultdict(set)
        sep='; '
        for i,row in df.iterrows():
            sample = extract_sample_id(row['File'])
            param = row[paramcol]
            val = row['Value']
            esd = row['ESD']
            if not sample or not param: continue
            if param in XRD_PARAM_MAPPING:
                colname = XRD_PARAM_MAPPING[param]
                data[sample][colname] = round(try_float(val) * 100,4)
                data[sample][colname+' ESD'] = round(try_float(esd) * 100,4)
            else:
                extra[sample].add(param)
        
        extra_str={k:sep.join(sorted(v)) for k,v in extra.items()}
        odf = pd.DataFrame(data).T.rename_axis('Sample')
        
        extra_col = XRD_PARAM_MAPPING['*']
        odf[extra_col] = extra_str
        odf[extra_col] = odf[extra_col].fillna('')
        return odf.sort_index()


    def read_crossreads_sheet(self):
        logger.debug("Reading CrossReads sheet from Google Spreadsheet")
        worksheet = self.spreadsheet.get_worksheet(0)
        rows = worksheet.get_all_values()
        df_big = pd.DataFrame.from_records(rows)
        df_big.columns = df_big.iloc[0]
        df_big = df_big.drop(0)

        # Remove rows with empty or NaN values in the first column
        first_column = df_big.columns[0]
        df_big = df_big.dropna(subset=[first_column])
        df_big = df_big[df_big[first_column] != ""]

        df_big = df_big.set_index(first_column)
        # df_big["numeric_id"] = [clean_sample_num(x) for x in df_big.index]
        # df_big = df_big.reset_index().set_index("numeric_id")
        logger.debug(f"Read {len(df_big)} rows from CrossReads sheet")
        return df_big

    def get_updated_data(self, df_xrd=None, df_meta=None):
        logger.debug("Updating CrossReads sheet with XRD data")
        
        if df_xrd is None: df_xrd = self.read_xrd_data()
        if df_meta is None: df_meta = self.read_crossreads_sheet()

        # Create a new dataframe with all columns from both df_meta and df_xrd
        cols = list(df_meta.columns) + [c for c in df_xrd if c not in set(df_meta.columns)]
        df_combined = df_meta.reindex(columns=cols)
        
        # Update common columns for existing rows and log changes
        updated_values=0
        updated_samples=set()
        for index in df_combined.index.intersection(df_xrd.index):
            for column in df_xrd.columns:
                old_value = df_combined.at[index, column]
                new_value = df_xrd.at[index, column]
                if value_was_updated(old_value, new_value):
                    df_combined.at[index, column] = new_value
                    logger.info(f"""[{index}] {column}: "{old_value}" -> "{new_value}" """)
                    updated_values+=1
                    updated_samples.add(index)
        logger.info(f'Updated {updated_values} values in {len(updated_samples)} samples')

        # Add new rows from df_xrd that don't exist in df_meta
        new_rows = df_xrd.loc[~df_xrd.index.isin(df_meta.index)]
        if not new_rows.empty:
            logger.info(f"Adding {len(new_rows)} new rows: {', '.join(new_rows.index)}")
        df_combined = pd.concat([df_combined, new_rows])
        
        # combined cols
        df_combined = self.calculate_combined_columns(df_combined)

        # Fill NaN with empty string
        return df_combined.fillna('').rename_axis(df_meta.index.name)

    def calculate_combined_columns(self, df_big):
        logger.debug("Calculating combined columns")
        df_big["XRD clay minerals"] = df_big.apply(
            lambda row: sum_columns(row, CLAY_MINERALS), axis=1
        )
        df_big["XRD K-feldspar"] = df_big.apply(
            lambda row: sum_columns(row, K_FELDSPAR), axis=1
        )
        df_big["XRD plagioclase"] = df_big.apply(
            lambda row: sum_columns(row, PLAGIOCLASE), axis=1
        )
        logger.debug(
            "Calculated XRD clay minerals, K-feldspar, and plagioclase columns"
        )
        return df_big

    def update_google_sheet(self, df_big):
        logger.debug(f"Updating Google Sheet with processed data ({len(df_big)} rows)")
        df_big = df_big.reset_index()
        worksheet = self.spreadsheet.get_worksheet(0)
        data_to_update = [df_big.columns.values.tolist()] + df_big.values.tolist()
        logger.debug(
            f"Preparing to update {len(data_to_update)} rows and {len(data_to_update[0])} columns"
        )
        res = worksheet.update(data_to_update)
        if not isinstance(res, dict) or not (
            res.get("spreadsheetId") and res.get("updatedCells")
        ):
            logger.warning("Error updating Google Sheets worksheet")
        else:
            logger.debug(
                f"Successfully updated {res['updatedCells']} cells in the Google Sheets worksheet."
            )

    def run(self):
        updated_data = self.get_updated_data()
        self.update_google_sheet(updated_data)

