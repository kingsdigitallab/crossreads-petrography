import unittest
from unittest.mock import patch, PropertyMock
import pandas as pd
from crossreads_petrography.pxrf import PXRFConverter
import plotnine as p9

class TestPXRFConverter(unittest.TestCase):
    def setUp(self):
        self.converter = PXRFConverter()

    @patch('crossreads_petrography.pxrf.read_path')
    def test_df_standards(self, mock_read_path):
        mock_df = pd.DataFrame({
            'standard': ['100CC', '50CC', '10CC', '0CC'],
            'Si': [0.00000, 55.23804, 84.34153, 90.64774],
            'K': [0.000000, 3.641829, 5.560614, 5.976381],
            'Ca': [100.000000, 39.644510, 7.844756, 0.954312],
            'Fe': [0.000000, 1.475631, 2.253103, 2.421567]
        })
        mock_read_path.return_value = mock_df

        result = self.converter.df_standards

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 4)  # Number of elements
        self.assertEqual(list(result.index), ['Si', 'K', 'Ca', 'Fe'])  # Elements as index
        self.assertIn('50CC', result.columns)
        self.assertIn('10CC', result.columns)
        self.assertIn('0CC', result.columns)
        self.assertIn('100CC', result.columns)
        # Check if the values are correctly transposed
        self.assertAlmostEqual(result.loc['Si', '50CC'], 55.23804)
        self.assertAlmostEqual(result.loc['Ca', '100CC'], 100.000000)

    @patch('crossreads_petrography.pxrf.read_path')
    def test_df_descriptions(self, mock_read_path):
        mock_df = pd.DataFrame({
            'instrument': ['site', 'day', 'month', 'year', 'cass', 'inv/id', 'Isic', 'a', 'b', 'c'],
            'CU': ['CU', '16', '2', '2022', 'epicum 3', 'a', '003248', '', '', ''],
            'marpo': ['marpo', '', '10', '2022', 'mag B', '74355', 'marpo74355', 'short edge, corner', 'long edge, corner', 'back'],
            'demo-MK.317': ['taormina', '22', '1', '2024', '', 'torso', '', 'under right armpit', 'left shoulder', 'right shoulder']
        })
        mock_read_path.return_value = mock_df

        result = self.converter.df_descriptions
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result.columns), 10)  # Number of columns (excluding index)
        self.assertIn('Isic', result.columns)
        self.assertIn('a', result.columns)

    @patch('crossreads_petrography.pxrf.read_path')
    def test_txt_input(self, mock_read_path):
        mock_txt = "SOURCE: 0-1.csv\nKEY: 1.1.00001.1\nElement Mass_fraction\nFe 0.5\nCa 0.3\n\nSOURCE: 0-2.csv\nKEY: 1.1.00001.2\nElement Mass_fraction\nFe 0.4\nCa 0.2"
        mock_read_path.return_value = mock_txt

        result = self.converter.txt_input

        self.assertEqual(result, mock_txt)

    @patch('crossreads_petrography.pxrf.PXRFConverter.txt_input', new_callable=PropertyMock)
    @patch('crossreads_petrography.pxrf.PXRFConverter.df_standards', new_callable=PropertyMock)
    def test_df_parsed(self, mock_df_standards, mock_txt_input):
        mock_txt_input.return_value = "Sample: 10-001.csv\nKey: Value\nElement Mass_fraction\nFe 0.5\nCa 0.3\n\nSample: 50-002.csv\nKey: Value\nElement Mass_fraction\nFe 0.4\nCa 0.2"
        mock_df_standards.return_value = pd.DataFrame({
            'Element': ['Fe', 'Ca'],
            '10CC': [1.0, 2.0],
            '50CC': [3.0, 4.0]
        }).set_index('Element')
        
        result = self.converter.df_parsed
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('Mass_fraction', result.columns)
        self.assertIn('standard_val', result.columns)
        self.assertIn('standard_group', result.columns)

    @patch('crossreads_petrography.pxrf.PXRFConverter.df_parsed', new_callable=PropertyMock)
    def test_df_linreg(self, mock_df_parsed):
        mock_df = pd.DataFrame({
            'Element': ['Fe', 'Ca', 'Fe', 'Ca'],
            'standard_group': ['10-50', '10-50', '50-100', '50-100'],
            'Mass_fraction': [0.5, 0.3, 0.4, 0.2],
            'standard_val': [1.0, 2.0, 3.0, 4.0]
        })
        mock_df_parsed.return_value = mock_df
        
        result = self.converter.df_linreg
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('m', result.columns)
        self.assertIn('q', result.columns)

    @patch('crossreads_petrography.pxrf.PXRFConverter.df_linreg', new_callable=PropertyMock)
    @patch('crossreads_petrography.pxrf.PXRFConverter.df_descriptions', new_callable=PropertyMock)
    @patch('crossreads_petrography.pxrf.PXRFConverter.txt_input', new_callable=PropertyMock)
    def test_df_adjusted(self, mock_txt_input, mock_df_descriptions, mock_df_linreg):
        mock_txt_input.return_value = "Sample: ISic001-A.csv\nKey: Value\nElement Mass_fraction\nFe 0.5\nCa 0.3\nSi 0.2\n\nSample: ISic002-B.csv\nKey: Value\nElement Mass_fraction\nFe 0.4\nCa 0.2\nSi 0.4"
        mock_df_descriptions.return_value = pd.DataFrame({
            'Isic': ['001', '002'],
            'A': ['Description 1', 'Description 2'],
            'B': ['Description 3', 'Description 4']
        })
        mock_df_linreg.return_value = pd.DataFrame({
            'Element': ['Fe', 'Ca', 'Si'],
            'standard_group': ['10-50', '10-50', '10-50'],
            'm': [1.0, 1.0, 1.0],
            'q': [0.0, 0.0, 0.0]
        })
        
        result = self.converter.df_adjusted
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('Calc_fraction', result.columns)
        self.assertIn('desc', result.columns)

    @patch('crossreads_petrography.pxrf.PXRFConverter.df_adjusted', new_callable=PropertyMock)
    @patch('crossreads_petrography.pxrf.pd.DataFrame.to_excel')
    def test_save(self, mock_to_excel, mock_df_adjusted):
        mock_df = pd.DataFrame({
            'Element': ['Fe', 'Ca'],
            'Calc_fraction': [50.0, 30.0],
            'desc': ['Description 1', 'Description 2']
        })
        mock_df_adjusted.return_value = mock_df
        
        self.converter.save()
        
        mock_to_excel.assert_called_once()

    @patch('crossreads_petrography.pxrf.PXRFConverter.save')
    def test_run(self, mock_save):
        self.converter.run()
        mock_save.assert_called_once()

    @patch('crossreads_petrography.pxrf.PXRFConverter.df_parsed', new_callable=PropertyMock)
    def test_plot(self, mock_df_parsed):
        mock_df = pd.DataFrame({
            'Element': ['Fe', 'Ca', 'Si', 'Fe', 'Ca', 'Si'],
            'Mass_fraction': [0.5, 0.3, 0.2, 0.4, 0.2, 0.4],
            'standard_val': [1.0, 2.0, 1.5, 3.0, 4.0, 3.5],
            'standard_group': ['10-50', '10-50', '10-50', '50-100', '50-100', '50-100']
        })
        mock_df_parsed.return_value = mock_df

        result = self.converter.plot()

        self.assertIsInstance(result, p9.ggplot)
        self.assertEqual(len(result.layers), 2)  # geom_point and geom_smooth
        self.assertEqual(result.mapping.get('x'), 'Mass_fraction')
        self.assertEqual(result.mapping.get('y'), 'standard_val')
        self.assertEqual(result.mapping.get('color'), 'standard_group')


if __name__ == '__main__':
    unittest.main()