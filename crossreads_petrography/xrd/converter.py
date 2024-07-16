from ..imports import *
from .constants import *
from .utils import *


class XRDConverter:
    def __init__(
        self,
        local_folder=None,
        remote_folder=None,
        credentials_path=None,
    ):
        self.local_folder = local_folder or PATH_XRD_INPUT_DATA
        self.remote_folder = remote_folder or PATH_XRD_INPUT_COLAB
        self.credentials_path = credentials_path or CREDENTIALS_PATH
        logger.debug(f"Initializing XRDConverter: {self.local_folder} / {self.remote_folder}")
        self.spreadsheet = get_spreadsheet(SPREADSHEET_URL)

    @cache
    def read_xrd_data(self):
        df = read_input_data_folder(self.local_folder if not IN_COLAB else self.remote_folder)
        paramcol = "Parameter, Goal"
        df = df[~df[paramcol].isin(COLS_TO_IGNORE)]

        data = defaultdict(dict)
        extra = defaultdict(set)
        sep = "; "
        for i, row in df.iterrows():
            sample = extract_sample_id(row["File"])
            param = row[paramcol]
            val = row["Value"]
            esd = row["ESD"]
            if not sample or not param:
                continue
            if param in XRD_PARAM_MAPPING:
                colname = XRD_PARAM_MAPPING[param]
                data[sample][colname] = round(try_float(val) * 100, 4)
                data[sample][colname + " ESD"] = round(try_float(esd) * 100, 4)
            else:
                extra[sample].add(param)

        extra_str = {k: sep.join(sorted(v)) for k, v in extra.items()}
        odf = pd.DataFrame(data).T.rename_axis("Sample")

        extra_col = XRD_PARAM_MAPPING["*"]
        odf[extra_col] = extra_str
        odf[extra_col] = odf[extra_col].fillna("")
        return odf.sort_index()

    def read_crossreads_sheet(self):
        logger.debug("Reading CrossReads sheet from Google Spreadsheet")
        return read_spreadsheet(self.spreadsheet)

    def get_updated_data(self, df_xrd=None, df_meta=None):
        logger.debug("Updating CrossReads sheet with XRD data")

        if df_xrd is None:
            df_xrd = self.read_xrd_data()
        if df_meta is None:
            df_meta = self.read_crossreads_sheet()

        # Create a new dataframe with all columns from both df_meta and df_xrd
        cols = list(df_meta.columns) + [
            c for c in df_xrd if c not in set(df_meta.columns)
        ]
        df_combined = df_meta.reindex(columns=cols)

        # Update common columns for existing rows and log changes
        updated_values = 0
        updated_samples = set()
        for index in df_combined.index.intersection(df_xrd.index):
            for column in df_xrd.columns:
                old_value = df_combined.at[index, column]
                new_value = df_xrd.at[index, column]
                if value_was_updated(old_value, new_value):
                    df_combined.at[index, column] = new_value
                    logger.info(
                        f"""[{index}] {column}: "{old_value}" -> "{new_value}" """
                    )
                    updated_values += 1
                    updated_samples.add(index)
        logger.info(
            f"Updated {updated_values} values in {len(updated_samples)} samples"
        )
        if not updated_values and not updated_samples: return  # return nothing if nothing updated

        # Add new rows from df_xrd that don't exist in df_meta
        new_rows = df_xrd.loc[~df_xrd.index.isin(df_meta.index)]
        if not new_rows.empty:
            logger.info(f"Adding {len(new_rows)} new rows: {', '.join(new_rows.index)}")
        df_combined = pd.concat([df_combined, new_rows])

        # combined cols
        df_combined = self.calculate_combined_columns(df_combined)

        # Fill NaN with empty string
        return df_combined.fillna("").rename_axis(df_meta.index.name)

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

    def update_google_sheet(self, df=None, worksheet_index=0):
        if df is None: df=self.get_updated_data()
        logger.debug(f"Updating Google Sheet with processed data ({len(df)} rows)")
        return update_spreadsheet(self.spreadsheet, df, worksheet_index=worksheet_index)

    def run(self):
        updated_data = self.get_updated_data()
        if updated_data is not None:
            self.update_google_sheet(updated_data)
