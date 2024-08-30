from . import *


class IsotopeConverter(CrossreadsPetrographyTool):
    name = "isotopes"

    @property
    def df_curves(self):
        logger.info(f"Reading isotope curve data from: {self.path_input}")
        df = read_path(self.path_input)
        logger.info(f"Loaded {len(df)} rows of isotope curve data")
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
        logger.info(f"Reshaped data into {len(reshaped_data)} points")
        return pd.DataFrame(reshaped_data).dropna()

    @property
    def df_points(self, xcol='isotopes delta13C', ycol='isotopes delta18O'):
        logger.info("Loading crossreads spreadsheet for isotope points")
        df_big = read_metadata(metamorphic=True).fillna('')
        logger.info(f"Loaded {len(df_big)} rows from crossreads spreadsheet")
        df_points = df_big[[xcol,ycol]].copy()
        df_points['Sample'] = [str(x) for x in df_points.index]
        df_points = df_points[~df_points.Sample.str.contains(' ')]
        df_points['y'] = df_points[xcol]
        df_points['x'] = df_points[ycol]
        df_points=df_points.reset_index()[['Sample','x','y']]
        df_points=df_points.query('Sample!="" & x!="" & y!=""')
        logger.info(f"Processed {len(df_points)} valid isotope points")
        return df_points.fillna('')
    
    @property
    def df_intersections(self):
        logger.info("Determining polygon intersections")
        intersections = determine_polygon_intersections(self.df_curves, self.df_points)
        logger.info(f"Found intersections for {len(intersections)} samples")
        return intersections
    
    def plot(self, output_folder=None):
        logger.info("Generating isotope plot")
        fig = plot_curves(self.df_curves, self.df_points)
        if output_folder:
            ofn_png=output_folder / 'isotope_graph.png'
            ofn_html=output_folder / 'isotope_graph.html'
            ofn_pdf=output_folder / 'isotope_graph.pdf'
            fig.write_image(ofn_png)
            logger.info(f'Saved PNG: {ofn_png}')
            fig.write_html(ofn_html)
            logger.info(f'Saved HTML: {ofn_html}')
            fig.write_image(ofn_pdf)
            logger.info(f'Saved PDF: {ofn_pdf}')
        return fig

    def save(self, output_folder=None):
        logger.info("Generating isotope outputs")        
        output_folder = output_folder or self.output_path_now
        logger.info(f"Using output folder: {output_folder}")
        
        ofn=Path(output_folder) / 'isotope_intersections.xlsx'
        self.df_intersections.to_excel(ofn)
        logger.info(f'Saved isotope intersections: {ofn}')

        self.plot(output_folder=output_folder)

    def run(self, output_folder=None):
        logger.info("Processing isotope data")
        self.save(output_folder)
        logger.info("Isotope data processing completed")



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
    logger.info("Determining polygon intersections")
    polygons = {marble_type: Polygon(zip(group['x'].values, group['y'].values))
                for marble_type, group in df_curves.groupby('marble_type')}
    logger.info(f"Created {len(polygons)} polygons for marble types")

    samples_list = df_points['Sample'].unique()
    marble_types = df_curves['marble_type'].unique()
    results_df = pd.DataFrame(index=samples_list, columns=marble_types)
    results_df = results_df.fillna('')

    intersected_count = 0
    for idx, row in df_points.iterrows():
        point = Point(row['x'], row['y'])
        intersected = False
        for marble_type, poly in polygons.items():
            if poly.contains(point):
                results_df.at[row['Sample'], marble_type] = '✔️'
                intersected = True
        if not intersected:
            results_df.loc[row['Sample']] = results_df.loc[row['Sample']].replace('', '✖️')
        else:
            intersected_count += 1

    logger.info(f"Found {intersected_count} samples intersecting with polygons")
    return results_df.sort_index(axis=1)