from ..imports import *
from .constants import *
from .utils import *
from functools import cached_property

class IsotopeConverter:
    def __init__(self):
        logger.info("Initializing IsotopeConverter")

    @cached_property
    def df_curves(self):
        logger.info("Reading isotope curve data from Google Sheets")
        return read_input_data_folder(PATH_ISOTOPE_INPUT_DATA if not IN_COLAB else PATH_ISOTOPE_INPUT_COLAB)

    @cached_property
    def df_samples(self):
        logger.info("Reading isotope sample data from Google Sheets")
        return read_spreadsheet(ISOTOPE_SAMPLES_URL)

    @cached_property
    def df_curves_reshaped(self):
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

    @cached_property
    def df_points(self):
        df = self.df_samples.copy()
        df['Sample'] = df['Sample'].apply(clean_sample_num)
        df = df[['Sample', 'x', 'y']]
        return df.query('Sample!="" & x!="" & y!=""')
    
    @cached_property
    def df_intersections(self):
        return determine_polygon_intersections(self.df_curves_reshaped, self.df_points)

    def plot(self, output_folder=None):
        fig = plot_curves(self.df_curves_reshaped, self.df_points)
        if output_folder:
            fig.write_html(output_folder / 'isotope_graph.html')
            fig.write_image(output_folder / 'isotope_graph.png')
            fig.write_image(output_folder / 'isotope_graph.pdf')
        return fig

    def generate_outputs(self, output_folder=None):
        logger.info("Generating isotope outputs")        
        output_folder = output_folder or PATH_ISOTOPE_OUTPUT
        self.df_intersections.to_excel(output_folder / 'isotope_intersections.xlsx')
        self.plot(output_folder=output_folder)

    def run(self, output_folder=PATH_ISOTOPE_OUTPUT):
        logger.info("Processing isotope data")
        self.generate_outputs(output_folder)