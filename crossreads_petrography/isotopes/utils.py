import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon
import plotly.graph_objects as go
from scipy.interpolate import splprep, splev

def clean_sample_num(x):
    if not x:
        return x
    x = x.strip().split()[0].split('-')[0]
    return ''.join(y for y in x if y.isdigit())

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