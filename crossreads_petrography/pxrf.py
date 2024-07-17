from .imports import *

PATH_PXRF_INPUT_DATA = PATH_INPUT_DATA / 'pXRF'
PATH_PXRF_INPUT_COLAB = '/content/drive/MyDrive/Crossreads B D1/pXRF input data'
PATH_PXRF_OUTPUT = PATH_OUTPUT_DATA / 'pXRF'
PATH_PXRF_OUTPUT.mkdir(parents=True, exist_ok=True)

PXRF_STANDARDS_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSkmTZ_k8VM_n3zcsxZrYsoAkleflLWIxLG2HpxU3kKIn7jszNIBwmPnDNLwiJ5yajYag6O-BTJz9Ey/pub?gid=0&single=true&output=csv'
PXRF_DESCRIPTIONS_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS6kznqXRhvtB9QuPgTKVFEy4EzhP_FEMocpcbILy8YH1GUu7X5Q0mm2WNvdxBUSQ/pub?gid=1673331354&single=true&output=csv'

class PXRFConverter:
    def __init__(self, input_file=None):
        logger.info("Initializing PXRFConverter")
        self.input_file = input_file or (PATH_PXRF_INPUT_DATA / '0-1_to_Sic003083-MK-c_concentrations.txt')

    @cached_property
    def df_standards(self):
        logger.info("Loading pXRF standard values")
        df = pd.read_csv(PXRF_STANDARDS_URL).set_index('standard')
        df = df.T.rename_axis('Element')
        return df[list(reversed(df.columns))]

    @cached_property
    def df_descriptions(self):
        logger.info("Loading pXRF descriptions")
        return pd.read_csv(PXRF_DESCRIPTIONS_URL).fillna('').set_index('instrument').T

    def parse_standards(self):
        logger.info("Parsing pXRF standards data")
        with open(self.input_file) as f:
            txt = f.read()
        
        o = []
        for srctxt in txt.strip().split('\n\n'):
            lines = srctxt.split('\n')
            src = lines[0].split(':')[-1].split('.csv')[0].strip()
            is_standard = src.replace('-', '').isdigit()
            if not is_standard:
                continue

            key = lines[1].split(':')[-1].strip()
            header = lines[2].split()
            data = [ln.split() for ln in lines[3:]]
            df = pd.DataFrame(data, columns=header).set_index('Element')

            standard_key = src.split('-')[0] + 'CC'
            df_this_standard = self.df_standards[[standard_key]].copy()
            df_this_standard.columns = ['standard_val']
            df_this_standard['standard_key'] = standard_key
            df_this_standard['source_name'] = src
            o.append(df.join(df_this_standard, how='inner'))

        df = pd.concat(o)
        df['Mass_fraction'] = pd.to_numeric(df['Mass_fraction'], errors='coerce')
        df['standard_val'] = pd.to_numeric(df['standard_val'], errors='coerce')

        df['standard_group'] = df['standard_key'].apply(lambda x: '10-50' if int(x.replace('CC', '')) < 60 else '50-100')
        return df[df.standard_key != '0CC']

    def get_standard_slope_intercept(self):
        logger.info("Calculating linear regressions for standard values")
        df = self.parse_standards()
        ld = []
        gby = ['Element', 'standard_group']
        for g, gdf in df.groupby(gby):
            X = gdf[['Mass_fraction']].values
            y = gdf['standard_val'].values

            model = LinearRegression()
            fit = model.fit(X, y)
            m = model.coef_[0]
            q = model.intercept_
            d = dict(zip(gby, g))
            d['m'] = m
            d['q'] = q
            ld.append(d)
        return pd.DataFrame(ld)

    def parse_measurements(self):
        logger.info("Parsing pXRF measurements and calculating new fractions")
        sdf = self.get_standard_slope_intercept()
        df_desc = self.df_descriptions

        with open(self.input_file) as f:
            txt = f.read()
        
        o = []
        for srctxt in txt.strip().split('\n\n'):
            lines = srctxt.split('\n')
            src = lines[0].split(':')[-1].split('.csv')[0].strip()
            is_standard = src.replace('-', '').isdigit()
            if is_standard:
                continue

            key = lines[1].split(':')[-1].strip()
            header = lines[2].split()
            data = [ln.split() for ln in lines[3:]]
            df = pd.DataFrame(data, columns=header).set_index('Element')
            df['Mass_fraction'] = pd.to_numeric(df['Mass_fraction'], errors='coerce')

            ca_si = df.loc['Ca']['Mass_fraction'] / df.loc['Si']['Mass_fraction']
            standard_group = '50-100' if ca_si >= 10 else '10-50'
            df['standard_group'] = standard_group
            df = df.merge(sdf, on=['Element', 'standard_group'], how='inner')
            df['y'] = (df['m'] * df['Mass_fraction']) + df['q']
            df['Calc_fraction'] = df['y'] / df['y'].sum() * 100
            df['source_name'] = src

            try:
                isic = src.split('-')[0][4:]
                isic_letter = src.split('-')[-1]

                desc_rows = df_desc[df_desc.Isic == isic]
                desc_col = desc_rows[isic_letter]
                desc = '; '.join(desc_col)
            except KeyError as e:
                logger.warning(f'Could not find {repr(isic_letter)} in logbook columns ({list(desc_rows.columns)})')
                desc = '?'

            df['desc'] = desc
            o.append(df)
        
        return pd.concat(o).set_index(['source_name', 'Element'])

    def save(self, output_folder=None):
        logger.info("Saving pXRF processed data")
        output_folder = output_folder or PATH_PXRF_OUTPUT
        df = self.parse_measurements()
        output_file = output_folder / 'pXRF_calculated_fractions.xlsx'
        df.to_excel(output_file)
        logger.info(f"Saved: {output_file}")

    def run(self, output_folder=PATH_PXRF_OUTPUT):
        logger.info("Processing pXRF data")
        self.save(output_folder)


def extract_sample_id(filename):
    noext = os.path.splitext(filename)[0]
    before, suffix = os.path.split(noext)
    if 'ISic' in before:
        return f'ISic{suffix}'
    return suffix

def clean_params(x):
    if x in {'Qcalcitemg', 'Qcalcitmg'}:
        return 'QMgCalcite'
    return x