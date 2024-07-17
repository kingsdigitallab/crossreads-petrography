from .imports import *

ISOTOPE_CURVES_URL = 'https://docs.google.com/spreadsheets/d/1P-NDhxRnLU8Tkg4dlXvef7DCYKE2qrSx/edit'
ISOTOPE_SAMPLES_URL = 'https://docs.google.com/spreadsheets/d/1N26mnpoRzENkesBL3uAAFfRp2uHCR0Dq/edit'

PATH_ISOTOPE_INPUT_DATA = PATH_INPUT_DATA / 'isotopes'
PATH_ISOTOPE_INPUT_COLAB = '/content/drive/MyDrive/Crossreads B D1/Isotope input data'
PATH_ISOTOPE_OUTPUT = PATH_OUTPUT_DATA / 'isotopes'
PATH_ISOTOPE_OUTPUT.mkdir(parents=True, exist_ok=True)

class IsotopeConverter:
    def __init__(self):
        logger.info("Initializing IsotopeConverter")

    @cached_property
    def df_curves(self):
        logger.info("Reading isotope curve data from Google Sheets")
        df = read_input_data_folder(PATH_ISOTOPE_INPUT_DATA if not IN_COLAB else PATH_ISOTOPE_INPUT_COLAB)
        df = df.replace({'':np.nan})
        types = {'_'.join(x.split('_')[:-1]) for x in df.columns}
        reshaped_data = []
        for _, row in df.iterrows():
            for typename in types:
                d = {'marble_type': typename}
                for coord in ['x', 'y']:
                    colname = f'{typename}_{coord}'
                    d[coord] = row[colname]
                reshaped_data.append(d)
        return pd.DataFrame(reshaped_data).dropna()

    @cached_property
    def df_samples(self):
        logger.info("Reading isotope sample data from Google Sheets")
        return read_spreadsheet(ISOTOPE_SAMPLES_URL)

    @cached_property
    def df_points(self, xcol='isotopes delta13C', ycol='isotopes delta18O'):
        df_big = read_crossreads_spreadsheet()
        df_points = df_big[[xcol,ycol]].copy()
        df_points['Sample'] = df_points.index
        df_points = df_points[~df_points.Sample.str.contains(' ')]
        df_points['y'] = df_points[xcol]
        df_points['x'] = df_points[ycol]
        df_points=df_points.reset_index()[['Sample','x','y']]
        df_points=df_points.query('Sample!="" & x!="" & y!=""')
        return df_points
    
    @cached_property
    def df_intersections(self):
        return determine_polygon_intersections(self.df_curves, self.df_points)

    def plot(self, output_folder=None):
        fig = plot_curves(self.df_curves, self.df_points)
        if output_folder:
            fig.write_html(output_folder / 'isotope_graph.html')
            fig.write_image(output_folder / 'isotope_graph.png')
            fig.write_image(output_folder / 'isotope_graph.pdf')
        return fig

    def save(self, output_folder=None):
        logger.info("Generating isotope outputs")        
        output_folder = output_folder or PATH_ISOTOPE_OUTPUT
        self.df_intersections.to_excel(output_folder / 'isotope_intersections.xlsx')
        self.plot(output_folder=output_folder)

    def run(self, output_folder=PATH_ISOTOPE_OUTPUT):
        logger.info("Processing isotope data")
        self.save(output_folder)



def plot_curves(df_curves, df_points):
    fig = go.Figure()

    for marble_type, group in df_curves.groupby('marble_type'):
        x_closed = np.append(group['x'].values, group['x'].values[0])
        y_closed = np.append(group['y'].values, group['y'].values[0])
        fig.add_trace(go.Scatter(
            x=x_closed,
            y=y_closed,
            fill='toself',
            name=marble_type,
            mode='lines'
        ))

    fig.add_trace(go.Scatter(
        x=df_points['x'],
        y=df_points['y'],
        mode='markers+text',
        text=df_points['Sample'],
        textposition='top center',
        marker=dict(size=10, color='red', symbol='circle'),
        name='Samples'
    ))

    fig.update_layout(
        title='Polygons for each marble type + points for marble samples',
        xaxis_title='d18O',
        yaxis_title='d13C',
        showlegend=True,
        height=800,
        width=1000
    )
    return fig

def determine_polygon_intersections(df_curves, df_points):
    polygons = {marble_type: Polygon(zip(group['x'].values, group['y'].values))
                for marble_type, group in df_curves.groupby('marble_type')}

    samples_list = df_points['Sample'].unique()
    marble_types = df_curves['marble_type'].unique()
    results_df = pd.DataFrame(index=samples_list, columns=marble_types)
    results_df = results_df.fillna('')

    for idx, row in df_points.iterrows():
        point = Point(row['x'], row['y'])
        intersected = False
        for marble_type, poly in polygons.items():
            if poly.contains(point):
                results_df.at[row['Sample'], marble_type] = '✔️'
                intersected = True
        if not intersected:
            results_df.loc[row['Sample']] = results_df.loc[row['Sample']].replace('', '✖️')

    return results_df.sort_index(axis=1)