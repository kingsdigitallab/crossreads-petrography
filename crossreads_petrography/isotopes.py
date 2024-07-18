from .imports import *
from .utils import *


class IsotopeConverter:
    def __init__(self):
        logger.info("Initializing IsotopeConverter")

    @cached_property
    def df_curves(self):
        logger.info("Reading isotope curve data")
        df = read_path('isotopes.polygons')
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
    def df_points(self, xcol='isotopes delta13C', ycol='isotopes delta18O'):
        df_big = read_crossreads_spreadsheet()
        df_points = df_big[[xcol,ycol]].copy()
        df_points['Sample'] = [str(x) for x in df_points.index]
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
            ofn_png=output_folder / 'isotope_graph.png'
            ofn_html=output_folder / 'isotope_graph.html'
            ofn_pdf=output_folder / 'isotope_graph.pdf'
            fig.write_image(ofn_png)
            logger.debug(f'Saved: {ofn_png.name}')

            fig.write_html(ofn_html)
            logger.debug(f'Saved: {ofn_html.name}')

            fig.write_image(ofn_pdf)
            logger.debug(f'Saved: {ofn_pdf.name}')
        return fig

    def save(self, output_folder=None):
        logger.info("Generating isotope outputs")        
        output_folder = output_folder or get_path('isotopes.output')
        ofn=Path(output_folder) / 'isotope_intersections.xlsx'
        self.df_intersections.to_excel(ofn)
        logger.debug(f'Saved: {ofn.name}')
        self.plot(output_folder=output_folder)

    def run(self, output_folder=None):
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