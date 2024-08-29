import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from crossreads_petrography import *
from unittest.mock import patch, PropertyMock
import pandas as pd
logger.setLevel(logging.DEBUG)

@pytest.fixture
def mgs_converter():
    return MgsConverter()

@patch('crossreads_petrography.mgs.read_path')
def test_df_input(mock_read_path, mgs_converter):
    mock_df = pd.DataFrame({
        'subtype': ['Goktepe', 'Docimian', 'Penteli'],
        'value_type': ['min wh', 'max wh', 'min box'],
        'value_mm': [1.0, 2.0, 1.5]
    })
    mock_read_path.return_value = mock_df
    
    result = mgs_converter.df_input
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert 'subtype' in result.columns
    assert 'value_type' in result.columns
    assert 'value_mm' in result.columns

@patch('crossreads_petrography.mgs.MgsConverter.df_input', new_callable=PropertyMock)
@patch('crossreads_petrography.mgs.read_metadata')
def test_df_output(mock_read_metadata, mock_df_input, mgs_converter):
    mock_df_input.return_value = pd.DataFrame({
        'subtype': ['Carrara'] * 5,
        'value_type': ['min wh', 'min box', 'median', 'max box', 'max wh'],
        'value_mm': [0.28, 0.49, 0.71, 1.01, 1.37]
    })
    
    mock_metadata = pd.DataFrame({
        'optical microscopy MGS (mm)': [1.2, 1.8, 2.2, 2.5, 3.0],
        'digital microscopy MGS (mm)': [1.3, 1.9, 2.3, 2.6, 3.1]
    }, index=['ISic001', 'ISic002', 'ISic003', 'ISic004', 'ISic005'])
    mock_read_metadata.return_value = mock_metadata
    
    result = mgs_converter.df_output
    print(result)
    
    assert isinstance(result, pd.DataFrame)
    assert 'Carrara' in result.columns
    assert 'ISic001' in result.index

@patch('crossreads_petrography.mgs.MgsConverter.df_output', new_callable=PropertyMock)
def test_save(mock_df_output, mgs_converter, tmp_path):
    mock_df = pd.DataFrame({
        'Göktepe': ['🔬', '🔍', ''],
        'Docimium': ['', '🔬🔍', '🔬'],
        'Pentelikon': ['🔍', '', '🔍']
    }, index=['ISic001', 'ISic002', 'ISic003'])
    mock_df_output.return_value = mock_df
    
    mgs_converter.path_output = tmp_path
    mgs_converter.save()
    
    expected_file = tmp_path / 'mgs_intersections.xlsx'
    assert expected_file.exists()

def test_run(mgs_converter):
    with patch.object(MgsConverter, 'save') as mock_save:
        mgs_converter.run()
        mock_save.assert_called_once()