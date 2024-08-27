from . import *

COLS_TO_IGNORE = {"Rwp", "Rexp", "Chi2", "GOF"}

## DEPRECATED: Getting this now from google sheets file

# XRD_PARAM_MAPPING = {
#     "Qcalcite": "XRD calcite content (%)",
#     "QMgCalcite": "XRD magnesian calcite content (%)",
#     "Qdolomite": "XRD dolomite content (%)",
#     "SiO2p3221": "XRD quartz content (%)",
#     "quartz": "XRD quartz content (%)",
#     "musc2m1": "XRD muscovite content (%)",
#     "Aragonite": "XRD aragonite content (%)",
#     "Hematite": "XRD Fe-oxihydroxides content (%)",
#     "HEMATITE": "XRD Fe-oxihydroxides content (%)",
#     "Lepidocrocite": "XRD Fe-oxihydroxides content (%)",
#     "Goethite": "XRD Fe-oxihydroxides content (%)",
#     "PYRITE": "XRD pyrite content (%)",
#     "Kaolinite1A": "XRD kaolinite content (%)",
#     "Kaolinitedis": "XRD kaolinite content (%)",
#     "Kaolid": "XRD kaolinite content (%)",
#     "smectitedi2wfix1": "XRD smectite content (%)",
#     "Chlorite2b": "XRD chlorite content (%)",
#     "Glauconite": "XRD glauconite content (%)",
#     "Glauconite_1": "XRD glauconite content (%)",
#     "Glauconite_2": "XRD glauconite content (%)",
#     "Glauconite_3": "XRD glauconite content (%)",
#     "Orthoclase": "XRD orthoclase content (%)",
#     "Orthoclase_1": "XRD orthoclase content (%)",
#     "Orthoclase_2": "XRD orthoclase content (%)",
#     "Orthoclase_3": "XRD orthoclase content (%)",
#     "MicroInt1": "XRD microcline content (%)",
#     "MicroInt2": "XRD microcline content (%)",
#     "MicroMax": "XRD microcline content (%)",
#     "SANINA85": "XRD Na-sanidine content (%)",
#     "Sanina75": "XRD Na-sanidine content (%)",
#     "SANINA67": "XRD Na-sanidine content (%)",
#     "SANINA56": "XRD Na-sanidine content (%)",
#     "SANINA35": "XRD Na-sanidine content (%)",
#     "Sanina16": "XRD Na-sanidine content (%)",
#     "SANINA07": "XRD Na-sanidine content (%)",
#     "Sanid086": "XRD K-sanidine content (%)",
#     "Sanid08": "XRD K-sanidine content (%)",
#     "Anorthoclase_1": "XRD anorthoclase content (%)",
#     "Anorthoclase_2": "XRD anorthoclase content (%)",
#     "Anorthoclase_3": "XRD anorthoclase content (%)",
#     "Anorthoclase_4": "XRD anorthoclase content (%)",
#     "Albite": "XRD albite content (%)",
#     "ANORTK33": "XRD albite content (%)",
#     "ANORTK25": "XRD albite content (%)",
#     "ANORTK15": "XRD albite content (%)",
#     "MONALBIT": "XRD albite content (%)",
#     "ALBINT": "XRD albite content (%)",
#     "Analbite": "XRD albite content (%)",
#     "Oligoclase_1": "XRD oligoclase content (%)",
#     "Oligoclase_2": "XRD oligoclase content (%)",
#     "Oligoclase_3": "XRD oligoclase content (%)",
#     "Oligoclase_4": "XRD oligoclase content (%)",
#     "Plag16an": "XRD oligoclase content (%)",
#     "Plag25an": "XRD oligoclase content (%)",
#     "Andesine_1": "XRD andesine content (%)",
#     "Andesine_2": "XRD andesine content (%)",
#     "Plag50": "XRD andesine content (%)",
#     "PLAG50C1": "XRD andesine content (%)",
#     "Plag65an": "XRD labradorite content (%)",
#     "Labradorite_1": "XRD labradorite content (%)",
#     "Labradorite_2": "XRD labradorite content (%)",
#     "Labradorite_3": "XRD labradorite content (%)",
#     "Labradorite_4": "XRD labradorite content (%)",
#     "Labradorite_5": "XRD labradorite content (%)",
#     "Bytownite": "XRD bytownite content (%)",
#     "Plag85an": "XRD bytownite content (%)",
#     "Anorthite": "XRD anorthite content (%)",
#     "Anorthite_1": "XRD anorthite content (%)",
#     "Anorthite_2": "XRD anorthite content (%)",
#     "Anorthite_3": "XRD anorthite content (%)",
#     "Anorthite_4": "XRD anorthite content (%)",
#     "Anorthite_5": "XRD anorthite content (%)",
#     "*": "XRD other minerals",
# }

# CLAY_MINERALS = [
#     "XRD kaolinite content (%)",
#     "XRD smectite content (%)",
#     "XRD chlorite content (%)",
#     "XRD glauconite content (%)",
# ]
# K_FELDSPAR = [
#     "XRD orthoclase content (%)",
#     "XRD microcline content (%)",
#     "XRD K-sanidine content (%)",
#     "XRD anorthoclase content (%)",
# ]
# PLAGIOCLASE = [
#     "XRD albite content (%)",
#     "XRD oligoclase content (%)",
#     "XRD andesine content (%)",
#     "XRD labradorite content (%)",
#     "XRD bytownite content (%)",
#     "XRD anorthite content (%)",
# ]


class XRDConverter:
    def __init__(
        self,
    ):
        logger.debug(f"Initializing XRDConverter")
        self.paths = {
            k[4:] if k[4:] else "xrd": v
            for k, v in config.paths.items()
            if k.startswith("xrd.")
        }

    @property
    def df_input(self):
        return read_path('xrd.input',sep=';').fillna('')
    
    @property
    def df_mineral_types(self):
        return read_path('xrd.mineral_types')
    
    @property
    def df_xrd(self):
        logger.debug("Reading XRD data")
        df = self.df_input
        paramcol = "Parameter, Goal"
        df = df[~df[paramcol].isin(COLS_TO_IGNORE)]
        df_params = self.df_mineral_types
        df_params["subtype"] = df_params["subtype"].apply(lambda x: x.lower())
        df_params = df_params.drop_duplicates("subtype")
        df_params = df_params.set_index("subtype")

        data = defaultdict(dict)
        extra = defaultdict(set)
        sep = "; "
        for i, row in df.iterrows():
            sample = extract_sample_id(row["File"])
            if not sample in data:
                data[sample] = Counter()
            param = row[paramcol].lower()
            val = row["Value"]
            esd = row["ESD"]
            if type(esd) is str and esd.endswith(","):
                esd = pd.to_numeric(esd[:-1])
            if esd > val:
                logger.warning(
                    f"ESD ({esd}) is larger than value ({val}) for {sample} on {param}"
                )
            if not sample or not param:
                continue
            if param in set(df_params.query('colname!=""').index):
                colname = str(df_params.loc[param]["colname"])
                data[sample][colname] += try_float(val) * 100
                data[sample][colname + " ESD"] += try_float(esd) * 100
            else:
                extra[sample].add(param.title())

        extra_str = {k: sep.join(sorted(v)) for k, v in extra.items()}
        odf = pd.DataFrame(data).T.rename_axis("Sample")

        extra_col = df_params.loc["*"]["colname"]
        odf[extra_col] = extra_str
        odf[extra_col] = odf[extra_col].fillna("")

        for cat, cat_df in df_params[df_params.category != ""].groupby("category"):
            cat_subtypes = cat_df.colname
            cat_colname = f"XRD {cat}"

            cat_sums = []
            for i, row in odf.iterrows():
                row_sum = 0
                for col in set(cat_subtypes):
                    val = row.get(col, 0)
                    if not np.isnan(val) and val:
                        row_sum += val
                cat_sums.append(row_sum)
            odf[cat_colname] = cat_sums

        return odf.sort_index().fillna("")

    ## DEPRECATED: No longer updating crossreads sheet directly

    # @property
    # def df_meta(self):
    #     logger.debug("Reading CrossReads sheet from Google Spreadsheet")
    #     return read_crossreads_spreadsheet()

    # @property
    # def df_updated(self):
    #     logger.debug("Updating CrossReads sheet with XRD data")

    #     df_xrd = self.df_xrd
    #     df_meta = self.df_meta

    #     # Create a new dataframe with all columns from both df_meta and df_xrd
    #     cols = list(df_meta.columns) + [
    #         c for c in df_xrd if c not in set(df_meta.columns)
    #     ]
    #     df_combined = df_meta.reindex(columns=cols)

    #     # Update common columns for existing rows and log changes
    #     updated_values = 0
    #     updated_samples = set()
    #     for index in df_combined.index.intersection(df_xrd.index):
    #         for column in df_xrd.columns:
    #             old_value = df_combined.at[index, column]
    #             new_value = df_xrd.at[index, column]
    #             if value_was_updated(old_value, new_value):
    #                 df_combined.at[index, column] = new_value
    #                 logger.info(
    #                     f"""[{index}] {column}: "{old_value}" -> "{new_value}" """
    #                 )
    #                 updated_values += 1
    #                 updated_samples.add(index)
    #     logger.info(
    #         f"Updated {updated_values} values in {len(updated_samples)} samples"
    #     )
    #     if not updated_values and not updated_samples:
    #         return  # return nothing if nothing updated

    #     # Add new rows from df_xrd that don't exist in df_meta
    #     new_rows = df_xrd.loc[~df_xrd.index.isin(df_meta.index)]
    #     if not new_rows.empty:
    #         logger.info(f"Adding {len(new_rows)} new rows: {', '.join(new_rows.index)}")
    #     df_combined = pd.concat([df_combined, new_rows])

    #     # combined cols
    #     df_combined = calculate_combined_columns(df_combined)

    #     # Fill NaN with empty string
    #     return df_combined.fillna("").rename_axis(df_meta.index.name)

    # def save_update(self, df=None):
    #     if df is None:
    #         df = self.df_updated
    #     if df is None:
    #         return
    #     logger.debug(f"Attempting to save data ({len(df)} rows)")
    #     if has_credentials():
    #         logger.debug("Credentials available. Updating Google Sheet.")
    #         try:
    #             spreadsheet = get_spreadsheet(config.paths.xrd.url)
    #             update_spreadsheet(spreadsheet, df)
    #             logger.debug(f"Saved to Google Sheet: {config.paths.xrd.url}")
    #         except Exception as e:
    #             logger.error(f"Failed to update Google Sheet: {str(e)}")
    #     else:
    #         logger.warning("No credentials available. Skipping Google Sheet update.")

    #     output_path = Path(config.paths.xrd.output.local)
    #     logger.debug(f"Saving to local file: {output_path}")
    #     output_path.parent.mkdir(parents=True, exist_ok=True)
    #     df.to_excel(output_path, index=False)

    def save(self, output_folder=None):
        logger.info("Postprocessing XRD data")
        output_folder = output_folder or get_path("xrd.output")
        ofn = Path(output_folder) / "xrd_data_postprocessed.xlsx"
        self.df_xrd.to_excel(ofn)
        logger.info(f"Saved: {ofn}")

    def run(self):
        self.save()


def try_float(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def clean_sample_num(x):
    if not x:
        return x
    x = x.strip().split()[0].split("-")[0]
    return "".join(y for y in x if y.isdigit())


def extract_sample_id(filename):
    noext = os.path.splitext(filename)[0]
    before, suffix = os.path.split(noext)
    if "ISic" in before:
        return f"ISic{suffix}"
    return suffix


def clean_params(x):
    if x in {"Qcalcitemg", "Qcalcitmg"}:
        return "QMgCalcite"
    return x


def sum_columns(row, columns):
    return sum(float(row.get(col, 0)) for col in columns if pd.notna(row.get(col)))


def is2(x):
    if x is np.nan:
        return False
    if not x:
        return False
    return True


def value_was_updated(x, y):
    x_f = try_float(x)
    y_f = try_float(y)
    x = str(x_f) if x_f is not np.nan else str(x)
    y = str(y_f) if y_f is not np.nan else str(y)
    if y == "nan":
        return False
    return x != y


## DEPRECATED: Doing this differently now, taking combined categories from google sheet file

# def calculate_combined_columns(df_big):
#     logger.debug("Calculating combined columns")
#     df_big["XRD clay minerals"] = df_big.apply(
#         lambda row: sum_columns(row, CLAY_MINERALS), axis=1
#     )
#     df_big["XRD K-feldspar"] = df_big.apply(
#         lambda row: sum_columns(row, K_FELDSPAR), axis=1
#     )
#     df_big["XRD plagioclase"] = df_big.apply(
#         lambda row: sum_columns(row, PLAGIOCLASE), axis=1
#     )
#     logger.debug("Calculated XRD clay minerals, K-feldspar, and plagioclase columns")
#     return df_big
