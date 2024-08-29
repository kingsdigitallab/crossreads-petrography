from . import *

COLS_TO_IGNORE = {"Rwp", "Rexp", "Chi2", "GOF"}

class XRDConverter(CrossreadsPetrographyTool):
    name = "xrd"

    def __init__(self, path_input=None, path_output=None, path_mineral_types=None, path=None):
        super().__init__(
            path=path,
            path_input=path_input,
            path_output=path_output,
            path_mineral_types=path_mineral_types,
        )

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
