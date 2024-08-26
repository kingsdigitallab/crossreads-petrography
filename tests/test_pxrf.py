import unittest
from unittest.mock import patch, PropertyMock
import pandas as pd
from crossreads_petrography.pxrf import PXRFConverter
import plotnine as p9
import pytest

class TestPXRFConverter:
    @pytest.fixture
    def converter(self):
        return PXRFConverter()

    @patch('crossreads_petrography.pxrf.read_path')
    def test_df_standards(self, mock_read_path, converter):
        # Create a mock DataFrame that matches the expected input
        mock_df = pd.DataFrame({
            'standard': ['100CC', '90CC', '80CC', '70CC', '60CC', '50CC', '40CC', '30CC', '20CC', '10CC', '0CC'],
            'SiO2': [0.00, 11.57, 21.53, 27.17, 32.97, 55.45, 64.45, 73.80, 78.82, 84.72, 91.04],
            'K2O': [0.00, 0.76, 1.42, 1.79, 2.15, 3.66, 4.22, 4.87, 5.32, 5.59, 6.00],
            'CaO': [99.87, 87.37, 76.59, 70.49, 64.64, 39.80, 30.01, 19.82, 14.34, 7.88, 0.00],
            'Fe2O3': [0.13, 0.30, 0.46, 0.55, 0.64, 1.09, 1.29, 1.52, 1.65, 1.81, 2.00]
        })
        mock_read_path.return_value = mock_df

        result = converter.df_standards

        assert isinstance(result, pd.DataFrame)
        assert len(result.columns) == 11  # All standards should be present
        assert list(result.index) == ['SiO2', 'K2O', 'CaO', 'Fe2O3']  # Elements as index
        assert list(result.columns) == ['0CC', '10CC', '20CC', '30CC', '40CC', '50CC', '60CC', '70CC', '80CC', '90CC', '100CC']  # Reversed order of standards
        assert result.loc['SiO2', '50CC'] == pytest.approx(55.45)
        assert result.loc['CaO', '100CC'] == pytest.approx(99.87)

    @patch('crossreads_petrography.pxrf.read_path')
    def test_df_descriptions(self, mock_read_path, converter):
        mock_df = pd.DataFrame({
            'Isic': ['CU', 'marpo', 'demo-MK.317'],
            'site': ['CU', 'marpo', 'taormina'],
            'day': ['16', '', '22'],
            'month': ['2', '10', '1'],
            'year': ['2022', '2022', '2024'],
            'cass': ['epicum 3', 'mag B', ''],
            'inv/id': ['a', '74355', 'torso'],
            'a': ['', 'short edge, corner', 'under right armpit'],
            'b': ['', 'long edge, corner', 'left shoulder'],
            'c': ['', 'back', 'right shoulder']
        })
        mock_read_path.return_value = mock_df

        result = converter.df_descriptions
        
        assert isinstance(result, pd.DataFrame)
        assert 'Isic' in result.columns
        assert 'a' in result.columns
        assert 'b' in result.columns

    @patch('crossreads_petrography.pxrf.read_path')
    def test_txt_input(self, mock_read_path, converter):
        mock_txt = [("file1.csv", "SOURCE: 0-1.csv\nKEY: 1.1.00001.1\nElement Mass_fraction\nFe 0.5\nCa 0.3"),
                    ("file2.csv", "SOURCE: 0-2.csv\nKEY: 1.1.00001.2\nElement Mass_fraction\nFe 0.4\nCa 0.2")]
        mock_read_path.return_value = mock_txt

        result = converter.txt_input

        assert result == mock_txt

    @patch('crossreads_petrography.pxrf.PXRFConverter.txt_input', new_callable=PropertyMock)
    def test_df_input(self, mock_txt_input, converter):
        mock_txt_input.return_value = [("file1.csv", "content1"), ("file2.csv", "content2")]
        
        result = converter.df_input
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert 'filename' in result.columns
        assert 'text' in result.columns

    @patch('crossreads_petrography.pxrf.PXRFConverter.txt_input', new_callable=PropertyMock)
    @patch('crossreads_petrography.pxrf.PXRFConverter.df_standards', new_callable=PropertyMock)
    def test_df_parsed(self, mock_df_standards, mock_txt_input, converter):
        mock_txt_input.return_value = [
            ("file1.csv", "Sample: t0-10CC-1.csv\nKey: Value\nElement Mass_fraction\nFe 0.5\nCa 0.3"),
            ("file2.csv", "Sample: t0-50CC-1.csv\nKey: Value\nElement Mass_fraction\nFe 0.4\nCa 0.2")
        ]
        mock_df_standards.return_value = pd.DataFrame({
            '10CC': [1.0, 2.0],
            '50CC': [3.0, 4.0]
        }, index=['Fe', 'Ca'])
        
        result = converter.df_parsed
        
        assert isinstance(result, pd.DataFrame)
        assert 'Mass_fraction' in result.columns
        assert 'standard_val' in result.columns
        assert 'standard_group' in result.columns
        assert 'filename' in result.columns

    @patch('crossreads_petrography.pxrf.PXRFConverter.df_parsed', new_callable=PropertyMock)
    def test_df_linreg(self, mock_df_parsed, converter):
        mock_df = pd.DataFrame({
            'Element': ['Fe', 'Ca', 'Fe', 'Ca'],
            'standard_group': ['10-50', '10-50', '50-100', '50-100'],
            'Mass_fraction': [0.5, 0.3, 0.4, 0.2],
            'standard_val': [1.0, 2.0, 3.0, 4.0]
        })
        mock_df_parsed.return_value = mock_df
        
        result = converter.df_linreg
        
        assert isinstance(result, pd.DataFrame)
        assert 'm' in result.columns
        assert 'q' in result.columns

    @patch('crossreads_petrography.pxrf.PXRFConverter.df_linreg', new_callable=PropertyMock)
    @patch('crossreads_petrography.pxrf.PXRFConverter.df_descriptions', new_callable=PropertyMock)
    @patch('crossreads_petrography.pxrf.PXRFConverter.txt_input', new_callable=PropertyMock)
    def test_df_adjusted(self, mock_txt_input, mock_df_descriptions, mock_df_linreg, converter):
        mock_txt_input.return_value = [("file1.csv", "Sample: ISic001-A.csv\nKey: Value\nElement Mass_fraction Fit_Area Sigma_Area\nFe 0.5 100 10\nCa 0.3 80 8\nSi 0.2 60 6"),
                                       ("file2.csv", "Sample: ISic002-B.csv\nKey: Value\nElement Mass_fraction Fit_Area Sigma_Area\nFe 0.4 90 9\nCa 0.2 70 7\nSi 0.4 80 8")]
        mock_df_descriptions.return_value = pd.DataFrame({
            'Isic': ['Isic000001', 'Isic000002'],
            'a': ['Description 1', 'Description 2'],
            'b': ['Description 3', 'Description 4']
        })
        mock_df_linreg.return_value = pd.DataFrame({
            'Element': ['Fe', 'Ca', 'Si'],
            'standard_group': ['10-50', '10-50', '10-50'],
            'm': [1.0, 1.0, 1.0],
            'q': [0.0, 0.0, 0.0]
        })

        result = converter.df_adjusted

        assert isinstance(result, pd.DataFrame)
        assert 'Calc_fraction' in result.columns
        assert 'desc' in result.columns
        assert result.index.names == ['source_name', 'Element']

    @patch('crossreads_petrography.pxrf.PXRFConverter.df_adjusted', new_callable=PropertyMock)
    @patch('crossreads_petrography.pxrf.pd.DataFrame.to_excel')
    def test_save(self, mock_to_excel, mock_df_adjusted, converter):
        mock_df = pd.DataFrame({
            'Element': ['Fe', 'Ca'],
            'Calc_fraction': [50.0, 30.0],
            'desc': ['Description 1', 'Description 2']
        })
        mock_df_adjusted.return_value = mock_df
        
        converter.save()
        
        mock_to_excel.assert_called_once()

    def test_run(self, converter):
        with patch('crossreads_petrography.pxrf.PXRFConverter.save') as mock_save:
            converter.run()
            mock_save.assert_called_once()

    @patch('crossreads_petrography.pxrf.PXRFConverter.df_parsed', new_callable=PropertyMock)
    def test_plot(self, mock_df_parsed, converter):
        mock_df = pd.DataFrame({
            'Element': ['Fe', 'Ca', 'Si', 'Fe', 'Ca', 'Si'],
            'Mass_fraction': [0.5, 0.3, 0.2, 0.4, 0.2, 0.4],
            'standard_val': [1.0, 2.0, 1.5, 3.0, 4.0, 3.5],
            'standard_group': ['10-50', '10-50', '10-50', '50-100', '50-100', '50-100']
        })
        mock_df_parsed.return_value = mock_df

        result = converter.plot()

        assert isinstance(result, p9.ggplot)
        assert len(result.layers) == 2  # geom_point and geom_smooth
        assert result.mapping.get('x') == 'Mass_fraction'
        assert result.mapping.get('y') == 'standard_val'
        assert result.mapping.get('color') == 'standard_group'

if __name__ == '__main__':
    pytest.main()