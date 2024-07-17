import unittest
from unittest.mock import patch, MagicMock
from crossreads_petrography.utils import *

class TestCrossreadsPetrographyUtils(unittest.TestCase):

    @patch('crossreads_petrography.utils.get_spreadsheet')
    def test_get_crossreads_spreadsheet(self, mock_get_spreadsheet):
        mock_get_spreadsheet.return_value = 'mock_spreadsheet'
        result = get_crossreads_spreadsheet()
        self.assertEqual(result, 'mock_spreadsheet')
        mock_get_spreadsheet.assert_called_once_with(SPREADSHEET_URL)

    @patch('crossreads_petrography.utils.read_spreadsheet')
    def test_read_crossreads_spreadsheet(self, mock_read_spreadsheet):
        mock_read_spreadsheet.return_value = pd.DataFrame()
        result = read_crossreads_spreadsheet()
        self.assertIsInstance(result, pd.DataFrame)
        mock_read_spreadsheet.assert_called_once_with(SPREADSHEET_URL, worksheet_index=0)

    @patch('crossreads_petrography.utils.gspread.authorize')
    @patch('crossreads_petrography.utils.service_account.Credentials.from_service_account_file')
    @patch('crossreads_petrography.utils.os.path.exists')
    def test_get_spreadsheet(self, mock_exists, mock_from_service_account_file, mock_authorize):
        mock_exists.return_value = True
        mock_creds = MagicMock()
        mock_from_service_account_file.return_value = mock_creds
        mock_gc = MagicMock()
        mock_authorize.return_value = mock_gc
        mock_gc.open_by_url.return_value = 'mock_spreadsheet'

        result = get_spreadsheet('mock_url', 'mock_credentials_path')
        self.assertEqual(result, 'mock_spreadsheet')
        mock_exists.assert_called_once_with('mock_credentials_path')
        mock_from_service_account_file.assert_called_once_with('mock_credentials_path', scopes=["https://www.googleapis.com/auth/spreadsheets"])
        mock_authorize.assert_called_once_with(mock_creds)
        mock_gc.open_by_url.assert_called_once_with('mock_url')

    @patch('crossreads_petrography.utils.get_spreadsheet')
    @patch('crossreads_petrography.utils.pd.DataFrame.from_records')
    def test_read_spreadsheet(self, mock_from_records, mock_get_spreadsheet):
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet
        mock_worksheet.get_all_values.return_value = [['header1', 'header2'], ['row1col1', 'row1col2']]
        mock_get_spreadsheet.return_value = mock_spreadsheet
        mock_from_records.return_value = pd.DataFrame([['header1', 'header2'], ['row1col1', 'row1col2']])

        result = read_spreadsheet('mock_spreadsheet_url')
        print(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.columns.tolist(), ['header2'])  # first header is now index
        self.assertEqual(result.index.name, 'header1')
        mock_get_spreadsheet.assert_called_once_with('mock_spreadsheet_url')
        mock_spreadsheet.get_worksheet.assert_called_once_with(0)
        mock_worksheet.get_all_values.assert_called_once()
        mock_from_records.assert_called_once_with([['header1', 'header2'], ['row1col1', 'row1col2']])

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

if __name__ == '__main__':
    unittest.main()