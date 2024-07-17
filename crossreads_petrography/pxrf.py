from .imports import *

PATH_PXRF_INPUT_DATA = PATH_INPUT_DATA / 'pXRF'
PATH_PXRF_INPUT_COLAB = '/content/drive/MyDrive/Crossreads B D1/pXRF input data'
PATH_PXRF_OUTPUT = PATH_OUTPUT_DATA / 'pXRF'
PATH_PXRF_OUTPUT.mkdir(parents=True, exist_ok=True)

PXRF_STANDARDS_URL = 'https://docs.google.com/spreadsheets/d/1qaGvCqD0bm8JoYTKXdb76b_EcMHwHenU5NomGQSOf_M/edit'
PXRF_DESCRIPTIONS_URL = 'https://docs.google.com/spreadsheets/d/1TEjZTq_jocxsLaFTpx0uf1txzJSPZWFNFGjhlcSdEKc/edit'

class PXRFConverter:
    def __init__(self, input_file=None):
        logger.info("Initializing PXRFConverter")
        self.local_folder = PATH_PXRF_INPUT_DATA
        self.remote_folder = PATH_PXRF_INPUT_COLAB
        self.input_folder = self.local_folder if not IN_COLAB else self.remote_folder

    @cached_property
    def df_standards(self):
        logger.info("Loading pXRF standard values")
        df = read_spreadsheet(PXRF_STANDARDS_URL)
        df = df.T.rename_axis('Element')
        return df[list(reversed(df.columns))]

    @cached_property
    def df_descriptions(self):
        logger.info("Loading pXRF descriptions")
        odf=read_spreadsheet(PXRF_DESCRIPTIONS_URL).T
        odf.columns=[x.strip() for x in odf]
        return odf
    
    @cached_property
    def txt_input(self):
        return read_input_data_folder_txt(self.input_folder)

    @cached_property
    def df_parsed(self):
        logger.info("Parsing pXRF standards data")
        txt = self.txt_input
        
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
    
    @cached_property
    def df_linreg(self):
        logger.info("Calculating linear regressions for standard values")
        df = self.df_parsed
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

    @cached_property
    def df_adjusted(self):
        logger.info("Parsing pXRF measurements and calculating new fractions")
        sdf = self.df_linreg
        df_desc = self.df_descriptions
        txt = self.txt_input
        
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

    def plot(self):
        # @title Plot linear regressions
        import plotnine as p9
        df=self.df_parsed
        fig=p9.ggplot(df.reset_index(), p9.aes(x='Mass_fraction', y='standard_val', color='standard_group'))
        fig+=p9.geom_point()
        fig+=p9.geom_smooth(method='lm')
        fig+=p9.facet_wrap('Element', scales='free')
        return fig

    def save(self, output_folder=None):
        logger.info("Saving pXRF processed data")
        output_folder = output_folder or PATH_PXRF_OUTPUT
        df = self.df_adjusted
        output_file = output_folder / 'pXRF_calculated_fractions.xlsx'
        df.to_excel(output_file)
        logger.info(f"Saved: {output_file}")

    def run(self, output_folder=PATH_PXRF_OUTPUT):
        logger.info("Processing pXRF data")
        self.save(output_folder)

