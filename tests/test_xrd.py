import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from crossreads_petrography.xrd import *

class TestXRDConverter(unittest.TestCase):
    def setUp(self):
        self.converter = XRDConverter()

    @patch('crossreads_petrography.xrd.read_input_data_folder')
    @patch('crossreads_petrography.xrd.get_crossreads_spreadsheet')
    def test_df_xrd(self, mock_get_spreadsheet, mock_read_folder):
        mock_df = pd.DataFrame({
            'File': ['ISic001.csv'] * 51,
            'Parameter, Goal': ['Qcalcite'] * 51,
            'Value': [0.5] * 51,
            'ESD': [0.01] * 51
        })
        mock_read_folder.return_value = mock_df
        
        result = self.converter.df_xrd
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 51)
        self.assertIn('XRD calcite content (%)', result.columns)

    @patch('crossreads_petrography.xrd.read_crossreads_spreadsheet')
    def test_df_meta(self, mock_read_crossreads_spreadsheet):
        mock_df = pd.DataFrame({'Sample': ['ISic001', 'ISic002']})
        mock_read_crossreads_spreadsheet.return_value = mock_df
        
        result = self.converter.df_meta
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        mock_read_crossreads_spreadsheet.assert_called_once()

    @patch('crossreads_petrography.xrd.XRDConverter.df_xrd', new_callable=PropertyMock)
    @patch('crossreads_petrography.xrd.XRDConverter.df_meta', new_callable=PropertyMock)
    def test_df_updated(self, mock_df_meta, mock_df_xrd):
        mock_df_xrd.return_value = pd.DataFrame({
            'Sample': ['ISic001', 'ISic002'],
            'XRD calcite content (%)': [50, 30]
        }).set_index('Sample')
        mock_df_meta.return_value = pd.DataFrame({
            'Sample': ['ISic001', 'ISic003'],
            'XRD calcite content (%)': [40, 20]
        }).set_index('Sample')
        
        result = self.converter.df_updated
        print(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        self.assertEqual(result.loc['ISic001', 'XRD calcite content (%)'], 50)

    @patch('crossreads_petrography.xrd.update_spreadsheet')
    @patch('crossreads_petrography.xrd.get_spreadsheet')
    @patch('crossreads_petrography.xrd.has_credentials')
    def test_save(self, mock_has_credentials, mock_get_spreadsheet, mock_update_spreadsheet):
        mock_df = pd.DataFrame({'Sample': ['ISic001', 'ISic002']})
        
        # Test when credentials are not available
        mock_has_credentials.return_value = False
        self.converter.save(mock_df)
        mock_has_credentials.assert_called_once()
        mock_get_spreadsheet.assert_not_called()
        mock_update_spreadsheet.assert_not_called()
        
        # Reset mocks
        mock_has_credentials.reset_mock()
        mock_get_spreadsheet.reset_mock()
        mock_update_spreadsheet.reset_mock()
        
        # Test when credentials are available
        mock_has_credentials.return_value = True
        mock_spreadsheet = MagicMock()
        mock_get_spreadsheet.return_value = mock_spreadsheet
        self.converter.save(mock_df)
        mock_has_credentials.assert_called_once()
        mock_get_spreadsheet.assert_called_once()
        mock_update_spreadsheet.assert_called_once_with(mock_spreadsheet, mock_df)

class TestHelperFunctions(unittest.TestCase):
    def test_try_float(self):
        self.assertEqual(try_float('1.5'), 1.5)
        self.assertTrue(np.isnan(try_float('abc')))

    def test_extract_sample_id(self):
        self.assertEqual(extract_sample_id('path/to/ISic001.csv'), 'ISic001')
        self.assertEqual(extract_sample_id('001.csv'), '001')

    def test_clean_params(self):
        self.assertEqual(clean_params('Qcalcitemg'), 'QMgCalcite')
        self.assertEqual(clean_params('Other'), 'Other')

    def test_sum_columns(self):
        row = {'A': 1, 'B': 2, 'C': 3}
        self.assertEqual(sum_columns(row, ['A', 'B']), 3)

    def test_is2(self):
        self.assertTrue(is2('value'))
        self.assertFalse(is2(''))
        self.assertFalse(is2(np.nan))

    def test_value_was_updated(self):
        self.assertTrue(value_was_updated('1', '2'))
        self.assertFalse(value_was_updated('1', '1'))
        self.assertFalse(value_was_updated('1', 'nan'))

    def test_calculate_combined_columns(self):
        df = pd.DataFrame({
            'XRD kaolinite content (%)': [10, 20],
            'XRD smectite content (%)': [5, 10],
            'XRD orthoclase content (%)': [15, 25],
            'XRD albite content (%)': [20, 30]
        })
        result = calculate_combined_columns(df)
        self.assertIn('XRD clay minerals', result.columns)
        self.assertIn('XRD K-feldspar', result.columns)
        self.assertIn('XRD plagioclase', result.columns)

if __name__ == '__main__':
    unittest.main()