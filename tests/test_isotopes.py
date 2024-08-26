import pytest
from unittest.mock import patch, PropertyMock, MagicMock
import pandas as pd
from crossreads_petrography.isotopes import *

@pytest.fixture
def converter():
    return IsotopeConverter()

def mock_read_crossreads_spreadsheet():
    return pd.DataFrame({
        'isotopes delta13C': [1, 2, 3],
        'isotopes delta18O': [4, 5, 6],
        'reference or rock id': ['ISic001', 'ISic002', 'ISic003']
    }).set_index('reference or rock id')

@pytest.mark.parametrize("numrows", [100])
@patch('crossreads_petrography.isotopes.read_path')
def test_df_curves(mock_read_folder, converter, numrows):
    mock_df = pd.DataFrame({
        'Naxos_x': list(range(numrows)),
        'Naxos_y': list(range(numrows)),
    })
    mock_read_folder.return_value = mock_df
    
    result = converter.df_curves
    
    assert isinstance(result, pd.DataFrame)
    assert 'marble_type' in result.columns
    assert 'x' in result.columns
    assert 'y' in result.columns
    assert len(result) == numrows

@patch('crossreads_petrography.isotopes.read_crossreads_spreadsheet')
def test_df_points(mock_read_crossreads, converter):
    mock_read_crossreads.return_value = mock_read_crossreads_spreadsheet()
    
    result = converter.df_points
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert 'x' in result.columns
    assert 'y' in result.columns
    assert 'Sample' in result.columns

@patch('crossreads_petrography.isotopes.IsotopeConverter.df_curves', new_callable=PropertyMock)
@patch('crossreads_petrography.isotopes.IsotopeConverter.df_points', new_callable=PropertyMock)
def test_df_intersections(mock_df_points, mock_df_curves, converter):
    mock_df_curves.return_value = pd.DataFrame({
        'marble_type': ['marble_type1'] * 4 + ['marble_type2'] * 4,
        'x': [0, 2, 2, 0, 0, 2, 2, 0],
        'y': [0, 0, 2, 2, 1, 1, 3, 3]
    })
    mock_df_points.return_value = pd.DataFrame({
        'Sample': ['ISic001', 'ISic002'],
        'x': [1, 3],
        'y': [1, 3]
    })
    
    result = converter.df_intersections
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert result.loc['ISic001', 'marble_type1'] == '✔️'
    assert result.loc['ISic002', 'marble_type1'] == '✖️'

@patch('crossreads_petrography.isotopes.read_crossreads_spreadsheet')
@patch('crossreads_petrography.isotopes.plot_curves')
def test_plot(mock_plot_curves, mock_read_crossreads, converter):
    mock_read_crossreads.return_value = mock_read_crossreads_spreadsheet()

    mock_plot_curves.return_value = 'mock_figure'
    result = converter.plot()
    assert result == 'mock_figure'
    mock_plot_curves.assert_called_once()

@patch('crossreads_petrography.isotopes.IsotopeConverter.df_intersections', new_callable=PropertyMock)
@patch('crossreads_petrography.isotopes.IsotopeConverter.df_intersections_mgs', new_callable=PropertyMock)
@patch('crossreads_petrography.isotopes.IsotopeConverter.plot')
def test_save(mock_plot, mock_df_intersections_mgs, mock_df_intersections, converter):
    mock_df = pd.DataFrame({'Sample': ['ISic001', 'ISic002']})
    mock_df_intersections.return_value = mock_df
    mock_df_intersections_mgs.return_value = mock_df
    mock_plot.return_value = MagicMock()
    
    with patch('pandas.DataFrame.to_excel') as mock_to_excel, \
         patch('plotly.graph_objects.Figure.write_image') as mock_write_image, \
         patch('plotly.graph_objects.Figure.write_html') as mock_write_html:
        converter.save()
        assert mock_to_excel.call_count == 2  # Called for both intersections and mgs
        mock_plot.assert_called_once()

def test_plot_curves():
    df_curves = pd.DataFrame({
        'marble_type': ['type1', 'type1', 'type2', 'type2'],
        'x': [0, 2, 0, 2],
        'y': [0, 2, 1, 3]
    })
    df_points = pd.DataFrame({
        'Sample': ['ISic001', 'ISic002'],
        'x': [1, 3],
        'y': [1, 3]
    })
    
    result = plot_curves(df_curves, df_points)
    
    assert result is not None
    # Add more specific assertions about the figure if needed

def test_determine_polygon_intersections():
    df_curves = pd.DataFrame({
        'marble_type': ['type1'] * 4 + ['type2'] * 4,
        'x': [0, 2, 2, 0, 0, 2, 2, 0],
        'y': [0, 0, 2, 2, 1, 1, 3, 3]
    })
    df_points = pd.DataFrame({
        'Sample': ['ISic001', 'ISic002'],
        'x': [1, 3],
        'y': [1, 3]
    })
    
    result = determine_polygon_intersections(df_curves, df_points)
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert result.loc['ISic001', 'type1'] == '✔️'
    assert result.loc['ISic002', 'type1'] == '✖️'