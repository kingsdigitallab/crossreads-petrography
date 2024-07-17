import unittest
from unittest.mock import patch, PropertyMock
from crossreads_petrography.pxrf import *

class TestPXRFConverter(unittest.TestCase):
    def setUp(self):
        self.converter = PXRFConverter()

    @patch('crossreads_petrography.pxrf.read_spreadsheet')
    def test_df_standards(self, mock_read_spreadsheet):
        mock_df = pd.DataFrame({
            'Element': ['Fe', 'Ca'],
            '10CC': [1.0, 2.0],
            '50CC': [3.0, 4.0]
        }).set_index('Element')
        mock_read_spreadsheet.return_value = mock_df.T
        
        result = self.converter.df_standards
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertIn('50CC', result.columns)
        self.assertIn('10CC', result.columns)

    @patch('crossreads_petrography.pxrf.read_spreadsheet')
    def test_df_descriptions(self, mock_read_spreadsheet):
        mock_df = pd.DataFrame({
            'instrument': ['CU', 'marpo'],
            'site': ['CU', 'marpo'],
            'day': ['16', ''],
            'month': ['2', '10'],
            'year': ['2022', '2022'],
            'cass': ['epicum 3', 'mag B'],
            'inv/id': ['a', '74355'],
            'Isic': ['003248', 'marpo74355'],
            'a': ['', 'short edge, corner'],
            'b': ['', 'long edge, corner'],
            'c': ['', 'back'],
            'tracer': [True, False],
            'demo': [False, True]
        }).set_index('instrument')
        mock_read_spreadsheet.return_value = mock_df
        
        result = self.converter.df_descriptions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), len(mock_df.columns))
        self.assertIn('a', result.index)

    @patch('crossreads_petrography.pxrf.read_input_data_folder_txt')
    def test_txt_input(self, mock_read_input_data_folder_txt):
        mock_txt = "Sample: ISic001.csv\nKey: Value\nElement Mass_fraction\nFe 0.5\nCa 0.3\n\nSample: ISic002.csv\nKey: Value\nElement Mass_fraction\nFe 0.4\nCa 0.2"
        mock_read_input_data_folder_txt.return_value = mock_txt
        
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


if __name__ == '__main__':
    unittest.main()