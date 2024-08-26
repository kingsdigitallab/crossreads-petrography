import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, PropertyMock, MagicMock
from crossreads_petrography.xrd import *

@pytest.fixture
def xrd_converter():
    return XRDConverter()

def test_df_input(xrd_converter):
    with patch('crossreads_petrography.xrd.read_path') as mock_read_path:
        mock_df = pd.DataFrame({
            'File': ['ISic001.csv'] * 51,
            'Parameter, Goal': ['Qcalcite'] * 51,
            'Value': [0.5] * 51,
            'ESD': [0.01] * 51
        })
        mock_read_path.return_value = mock_df
        
        result = xrd_converter.df_input
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 51
        assert 'Parameter, Goal' in result.columns

def test_df_mineral_types(xrd_converter):
    with patch('crossreads_petrography.xrd.read_path') as mock_read_path:
        mock_df = pd.DataFrame({
            'subtype': ['Qcalcite', 'Qquartz'],
            'colname': ['XRD calcite content (%)', 'XRD quartz content (%)'],
            'category': ['', '']
        })
        mock_read_path.return_value = mock_df
        
        result = xrd_converter.df_mineral_types
        
        assert isinstance(result, pd.DataFrame)
        assert 'subtype' in result.columns
        assert 'colname' in result.columns
        assert 'category' in result.columns

def test_df_xrd(xrd_converter):
    with patch.object(XRDConverter, 'df_input', new_callable=PropertyMock) as mock_df_input, \
         patch.object(XRDConverter, 'df_mineral_types', new_callable=PropertyMock) as mock_df_mineral_types:
        
        mock_df_input.return_value = pd.DataFrame({
            'File': ['ISic001.csv'],
            'Parameter, Goal': ['Qcalcite'],
            'Value': [0.5],
            'ESD': [0.01]
        })
        mock_df_mineral_types.return_value = pd.DataFrame({
            'subtype': ['qcalcite', '*'],
            'colname': ['XRD calcite content (%)', 'XRD other minerals'],
            'category': ['', '']
        })
        
        result = xrd_converter.df_xrd
        
        assert isinstance(result, pd.DataFrame)
        assert 'XRD calcite content (%)' in result.columns
        assert 'XRD calcite content (%) ESD' in result.columns
        assert 'XRD other minerals' in result.columns

def test_save(xrd_converter, tmp_path):
    with patch.object(XRDConverter, 'df_xrd', new_callable=PropertyMock) as mock_df_xrd:
        mock_df_xrd.return_value = pd.DataFrame({
            'Sample': ['ISic001', 'ISic002'],
            'XRD calcite content (%)': [50, 30]
        }).set_index('Sample')
        
        output_folder = tmp_path / "output"
        output_folder.mkdir()
        xrd_converter.save(output_folder)
        
        assert (output_folder / "xrd_data_postprocessed.xlsx").exists()

def test_run(xrd_converter):
    with patch.object(XRDConverter, 'save') as mock_save:
        xrd_converter.run()
        mock_save.assert_called_once()

def test_try_float():
    assert try_float('1.5') == 1.5
    assert np.isnan(try_float('abc'))

def test_extract_sample_id():
    assert extract_sample_id('path/to/ISic001.csv') == 'ISic001'
    assert extract_sample_id('001.csv') == '001'

def test_clean_params():
    assert clean_params('Qcalcitemg') == 'QMgCalcite'
    assert clean_params('Qcalcitmg') == 'QMgCalcite'
    assert clean_params('Other') == 'Other'

def test_sum_columns():
    row = {'A': 1, 'B': 2, 'C': 3}
    assert sum_columns(row, ['A', 'B']) == 3

def test_is2():
    assert is2('value') == True
    assert is2('') == False
    assert is2(np.nan) == False

def test_value_was_updated():
    assert value_was_updated('1', '2') == True
    assert value_was_updated('1', '1') == False
    assert value_was_updated('1', 'nan') == False

def test_reads():
    with patch('crossreads_petrography.xrd.read_path') as mock_read_path:
        mock_df = pd.DataFrame({
            'File': ['ISic001.csv'],
            'Parameter, Goal': ['Qcalcite'],
            'Value': [0.5],
            'ESD': [0.01]
        })
        mock_read_path.return_value = mock_df
        
        df = read_path('xrd.input', sep=';')
        assert isinstance(df, pd.DataFrame)
        assert 'Parameter, Goal' in set(df.columns)