from ..imports import *

class IsotopeConverter:
    def __init__(self):
        logger.info("Initializing IsotopeConverter")
        self.authenticate()

    def authenticate(self):
        logger.info("Authenticating and accessing Google Spreadsheet")
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_PATH, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        self.client = gspread.authorize(creds)

    def read_isotope_data(self):
        logger.info("Reading isotope data from Google Sheets")
        self.df_curves = self.read_sheet(ISOTOPE_CURVES_URL)
        self.df_samples = self.read_sheet(ISOTOPE_SAMPLES_URL)

    def read_sheet(self, url):
        sheet = self.client.open_by_url(url).sheet1
        data = sheet.get_all_values()
        return pd.DataFrame(data[1:], columns=data[0])

    def process_data(self):
        logger.info("Processing isotope data")
        self.df_curves_reshaped = self.reshape_curves()
        self.df_points = self.process_samples()

    def reshape_curves(self):
        types = {x.split('_')[0] for x in self.df_curves.columns}
        reshaped_data = []
        for _, row in self.df_curves.iterrows():
            for typename in types:
                d = {'marble_type': typename}
                for coord in ['x', 'y']:
                    colname = f'{typename}_{coord}'
                    d[coord] = row[colname]
                reshaped_data.append(d)
        return pd.DataFrame(reshaped_data).dropna()

    def process_samples(self):
        df = self.df_samples.copy()
        df['Sample'] = df['Sample'].apply(clean_sample_num)
        df = df[['Sample', 'x', 'y']]
        return df.query('Sample!="" & x!="" & y!=""')

    def generate_outputs(self, output_folder):
        logger.info("Generating isotope outputs")
        fig = plot_curves(self.df_curves_reshaped, self.df_points, output_folder)
        fig.show()

        results_df = determine_polygon_intersections(self.df_curves_reshaped, self.df_points)
        results_df.to_excel(output_folder / 'isotope_intersections.xlsx')

    def run(self, output_folder=PATH_ISOTOPE_OUTPUT):
        self.read_isotope_data()
        self.process_data()
        self.generate_outputs(output_folder)