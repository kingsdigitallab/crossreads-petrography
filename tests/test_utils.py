from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from crossreads_petrography import *


import unittest
from unittest.mock import patch, MagicMock
import crossreads_petrography.utils
from crossreads_petrography.utils import *
import tempfile
import os

class TestCrossreadsPetrographyUtils(unittest.TestCase):

    @patch('crossreads_petrography.utils.get_path')
    @patch('crossreads_petrography.utils.get_spreadsheet')
    @patch('crossreads_petrography.utils.has_credentials')
    def test_get_crossreads_spreadsheet(self, mock_has_credentials, mock_get_spreadsheet, mock_get_path):
        mock_has_credentials.return_value = True
        mock_get_path.return_value = 'http://mock_url.com'
        mock_get_spreadsheet.return_value = 'mock_spreadsheet'
        result = get_crossreads_spreadsheet()
        self.assertEqual(result, 'mock_spreadsheet')
        mock_get_spreadsheet.assert_called_once_with('http://mock_url.com')

    @patch('crossreads_petrography.utils.read_path')
    def test_read_crossreads_spreadsheet(self, mock_read_path):
        mock_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        mock_read_path.return_value = mock_df
        result = read_crossreads_spreadsheet()
        self.assertIsInstance(result, pd.DataFrame)
        mock_read_path.assert_called_once_with('metadata.metamorphic')
        pd.testing.assert_frame_equal(result, mock_df.set_index(mock_df.columns[0]))

    @patch('crossreads_petrography.utils.IN_COLAB', False)
    @patch('crossreads_petrography.utils.Path')
    @patch('crossreads_petrography.utils.authenticate_service_account')
    @patch('crossreads_petrography.utils.gspread.authorize')
    @patch('crossreads_petrography.utils.has_credentials')
    def test_get_spreadsheet(self, mock_has_credentials, mock_authorize, mock_authenticate, mock_path):
        mock_has_credentials.return_value = True
        mock_path.return_value.exists.return_value = True
        mock_creds = MagicMock()
        mock_authenticate.return_value = mock_creds
        mock_gc = MagicMock()
        mock_authorize.return_value = mock_gc
        mock_gc.open_by_url.return_value = 'mock_spreadsheet'

        result = get_spreadsheet('mock_url', 'mock_credentials_path')
        self.assertEqual(result, 'mock_spreadsheet')
        mock_path.assert_called_once_with('mock_credentials_path')
        mock_path.return_value.exists.assert_called_once()
        mock_authenticate.assert_called_once_with('mock_credentials_path')
        mock_authorize.assert_called_once_with(mock_creds)
        mock_gc.open_by_url.assert_called_once_with('mock_url')

    @patch('crossreads_petrography.utils.IN_COLAB', False)
    @patch('crossreads_petrography.utils.has_credentials')
    def test_get_spreadsheet_no_credentials(self, mock_has_credentials):
        mock_has_credentials.return_value = False
        
        with self.assertRaises(ValueError) as context:
            get_spreadsheet('mock_url')
        
        self.assertEqual(str(context.exception), "No credentials available. Unable to access spreadsheet.")

    @patch('crossreads_petrography.utils.IN_COLAB', False)
    @patch('crossreads_petrography.utils.Path')
    @patch('crossreads_petrography.utils.has_credentials')
    def test_get_spreadsheet_credentials_not_found(self, mock_has_credentials, mock_path):
        mock_has_credentials.return_value = True
        mock_path.return_value.exists.return_value = False
        
        with self.assertRaises(FileNotFoundError) as context:
            get_spreadsheet('mock_url', 'mock_credentials_path')
        
        self.assertEqual(str(context.exception), "Credentials file not found: mock_credentials_path")
        mock_path.assert_called_once_with('mock_credentials_path')
        mock_path.return_value.exists.assert_called_once()

    @patch('crossreads_petrography.utils.IN_COLAB', True)
    @patch('crossreads_petrography.utils.has_credentials')
    @patch('crossreads_petrography.utils.authenticate_colab')
    @patch('crossreads_petrography.utils.gspread.authorize')
    def test_get_spreadsheet_colab(self, mock_authorize, mock_authenticate_colab, mock_has_credentials):
        mock_has_credentials.return_value = True
        mock_creds = MagicMock()
        mock_authenticate_colab.return_value = mock_creds
        mock_gc = MagicMock()
        mock_authorize.return_value = mock_gc
        mock_gc.open_by_url.return_value = 'mock_spreadsheet'

        result = get_spreadsheet('mock_url')
        self.assertEqual(result, 'mock_spreadsheet')
        mock_authenticate_colab.assert_called_once()
        mock_authorize.assert_called_once_with(mock_creds)
        mock_gc.open_by_url.assert_called_once_with('mock_url')

    @patch('crossreads_petrography.utils.get_spreadsheet')
    def test_read_spreadsheet(self, mock_get_spreadsheet):
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet
        mock_worksheet.get_all_values.return_value = [['header1', 'header2'], ['row1col1', 'row1col2']]
        mock_get_spreadsheet.return_value = mock_spreadsheet

        result = read_spreadsheet('mock_spreadsheet_url')
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.columns.tolist(), ['header1', 'header2'])
        self.assertEqual(result.values.tolist(), [['row1col1', 'row1col2']])
        mock_get_spreadsheet.assert_called_once_with('mock_spreadsheet_url')

    def test_read_spreadsheet_with_empty_rows(self):
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet
        mock_worksheet.get_all_values.return_value = [
            ['header1', 'header2'],
            ['row1col1', 'row1col2'],
            ['', ''],
            ['row2col1', 'row2col2']
        ]

        result = read_spreadsheet(mock_spreadsheet)
        self.assertEqual(len(result), 2)
        self.assertEqual(result['header1'].tolist(), ['row1col1', 'row2col1'])

    @patch('crossreads_petrography.utils.get_path')
    @patch('crossreads_petrography.utils.is_urllike')
    @patch('crossreads_petrography.utils.is_pathlike')
    @patch('crossreads_petrography.utils.read_spreadsheet')
    @patch('crossreads_petrography.utils.read_df')
    def test_read_path(self, mock_read_df, mock_read_spreadsheet, mock_is_pathlike, mock_is_urllike, mock_get_path):
        mock_get_path.return_value = 'mock_path'
        mock_is_urllike.return_value = False
        mock_is_pathlike.return_value = True
        mock_read_df.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

        result = read_path('mock_key')
        self.assertIsInstance(result, pd.DataFrame)
        assert len(result) == 0

    @patch('crossreads_petrography.utils.gspread.Spreadsheet')
    def test_update_spreadsheet(self, mock_spreadsheet):
        mock_worksheet = MagicMock()
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet
        mock_worksheet.update.return_value = {'spreadsheetId': 'mock_id', 'updatedCells': 2}
        df = pd.DataFrame({'header1': ['row1col1'], 'header2': ['row1col2']}).set_index('header1')

        update_spreadsheet(mock_spreadsheet, df)
        mock_spreadsheet.get_worksheet.assert_called_once_with(0)
        mock_worksheet.update.assert_called_once_with([['header1', 'header2'], ['row1col1', 'row1col2']])

    def test_read_df_csv(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data='header1,header2\nrow1col1,row1col2')) as mock_file:
            df = read_df('mock_file.csv')
            self.assertIsInstance(df, pd.DataFrame)
            self.assertEqual(df.columns.tolist(), ['header1', 'header2'])
            self.assertEqual(df.iloc[0].tolist(), ['row1col1', 'row1col2'])

    def test_read_df_excel(self):
        with patch('pandas.read_excel') as mock_read_excel:
            mock_read_excel.return_value = pd.DataFrame({'header1': ['row1col1'], 'header2': ['row1col2']})
            df = read_df('mock_file.xlsx')
            self.assertIsInstance(df, pd.DataFrame)
            self.assertEqual(df.columns.tolist(), ['header1', 'header2'])
            self.assertEqual(df.iloc[0].tolist(), ['row1col1', 'row1col2'])

    @patch('crossreads_petrography.utils.os.listdir')
    @patch('crossreads_petrography.utils.read_df')
    def test_read_input_data_folder(self, mock_read_df, mock_listdir):
        mock_listdir.return_value = ['file1.csv', 'file2.xlsx']
        mock_read_df.side_effect = [
            pd.DataFrame({'header1': ['row1col1'], 'header2': ['row1col2']}),
            pd.DataFrame({'header1': ['row2col1'], 'header2': ['row2col2']})
        ]

        with patch('crossreads_petrography.utils.IN_COLAB', False):
            df = read_input_data_folder('mock_folder')
            self.assertIsInstance(df, pd.DataFrame)
            self.assertEqual(len(df), 2)
            self.assertEqual(df.iloc[0].tolist(), ['row1col1', 'row1col2'])
            self.assertEqual(df.iloc[1].tolist(), ['row2col1', 'row2col2'])


    @patch('crossreads_petrography.utils.IN_COLAB', True)
    @patch('crossreads_petrography.utils.gspread.authorize')
    @patch('crossreads_petrography.utils.auth', MagicMock())
    @patch('crossreads_petrography.utils.default', MagicMock(return_value=(MagicMock(), None)))
    def test_get_spreadsheet_colab(self, mock_authorize):
        mock_gc = MagicMock()
        mock_authorize.return_value = mock_gc
        mock_gc.open_by_url.return_value = 'mock_spreadsheet'

        from crossreads_petrography.utils import get_spreadsheet
        
        result = get_spreadsheet('mock_url')
        self.assertEqual(result, 'mock_spreadsheet')
        mock_authorize.assert_called_once()
        mock_gc.open_by_url.assert_called_once_with('mock_url')

    @patch('crossreads_petrography.utils.IN_COLAB', True)
    @patch('crossreads_petrography.utils.os.listdir')
    @patch('crossreads_petrography.utils.read_df')
    @patch('crossreads_petrography.utils.drive', MagicMock())
    def test_read_input_data_folder_colab(self, mock_read_df, mock_listdir):
        mock_listdir.return_value = ['file1.csv', 'file2.xlsx']
        mock_read_df.side_effect = [
            pd.DataFrame({'header1': ['row1col1'], 'header2': ['row1col2']}),
            pd.DataFrame({'header1': ['row2col1'], 'header2': ['row2col2']})
        ]

        from crossreads_petrography.utils import read_input_data_folder
        
        df = read_input_data_folder('mock_folder')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        crossreads_petrography.utils.drive.mount.assert_called_once_with('/content/drive')

    def test_read_df_tsv(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tsv', delete=False) as tmp_file:
            tmp_file.write("header1\theader2\nrow1col1\trow1col2")
            tmp_file.flush()
            
            df = read_df(tmp_file.name)
            self.assertIsInstance(df, pd.DataFrame)
            self.assertEqual(df.columns.tolist(), ['header1', 'header2'])
            self.assertEqual(df.iloc[0].tolist(), ['row1col1', 'row1col2'])
        
        os.unlink(tmp_file.name)

    def test_read_df_unsupported_format(self):
        with self.assertRaises(ValueError):
            read_df('unsupported_file.txt')

    @patch('crossreads_petrography.utils.IN_COLAB', False)
    @patch('crossreads_petrography.utils.os.listdir')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="Sample text data")
    def test_read_input_data_folder_txt(self, mock_open, mock_listdir):
        mock_listdir.return_value = ['file1.txt', 'file2.txt']
        result = read_input_data_folder_txt('mock_folder')
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Sample text data\n\n\n\nSample text data")

    @patch('crossreads_petrography.utils.IN_COLAB', False)
    @patch('crossreads_petrography.utils.Path')
    @patch('crossreads_petrography.utils.has_credentials')
    def test_get_spreadsheet_credentials_not_found(self, mock_has_credentials, mock_path):
        mock_has_credentials.return_value = True
        mock_path.return_value.exists.return_value = False

        with self.assertRaises(FileNotFoundError):
            get_spreadsheet('mock_url', 'mock_credentials_path')

        mock_path.assert_called_once_with('mock_credentials_path')
        mock_path.return_value.exists.assert_called_once()

if __name__ == '__main__':
    unittest.main()