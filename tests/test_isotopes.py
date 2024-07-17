import unittest
from unittest.mock import patch, PropertyMock
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon
from crossreads_petrography.isotopes import *

class TestIsotopeConverter(unittest.TestCase):
    def setUp(self):
        self.converter = IsotopeConverter()

    @patch('crossreads_petrography.isotopes.read_input_data_folder')
    def test_df_curves(self, mock_read_folder):
        mock_df = pd.DataFrame({
            'marble_type1_x': [1, 2, 3, 4], 'marble_type1_y': [3, 4, 5, 6],
            'marble_type2_x': [5, 6, 7, 8], 'marble_type2_y': [7, 8, 9, 10]
        })
        mock_read_folder.return_value = mock_df
        
        result = self.converter.df_curves
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('marble_type', result.columns)
        self.assertIn('x', result.columns)
        self.assertIn('y', result.columns)
        self.assertEqual(len(result), 8)  # 4 rows * 2 marble types
        self.assertTrue(set(result['marble_type'].unique()) == {'marble_type1', 'marble_type2'})
        self.assertTrue(all(result['x'].isin([1, 2, 3, 4, 5, 6, 7, 8])))
        self.assertTrue(all(result['y'].isin([3, 4, 5, 6, 7, 8, 9, 10])))

    @patch('crossreads_petrography.isotopes.read_spreadsheet')
    def test_df_samples(self, mock_read_spreadsheet):
        mock_df = pd.DataFrame({'Sample': ['ISic001', 'ISic002']})
        mock_read_spreadsheet.return_value = mock_df
        
        result = self.converter.df_samples
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)

    @patch('crossreads_petrography.isotopes.read_crossreads_spreadsheet')
    def test_df_points(self, mock_read_crossreads):
        mock_df = pd.DataFrame({
            'isotopes delta13C': [1, 2],
            'isotopes delta18O': [3, 4]
        }, index=['ISic001', 'ISic002'])
        mock_read_crossreads.return_value = mock_df
        
        result = self.converter.df_points
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertIn('Sample', result.columns)
        self.assertIn('x', result.columns)
        self.assertIn('y', result.columns)

    @patch('crossreads_petrography.isotopes.IsotopeConverter.df_curves', new_callable=PropertyMock)
    @patch('crossreads_petrography.isotopes.IsotopeConverter.df_points', new_callable=PropertyMock)
    def test_df_intersections(self, mock_df_points, mock_df_curves):
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
        
        result = self.converter.df_intersections
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertEqual(result.loc['ISic001', 'marble_type1'], '✔️')
        self.assertEqual(result.loc['ISic002', 'marble_type1'], '✖️')

    @patch('crossreads_petrography.isotopes.plot_curves')
    def test_plot(self, mock_plot_curves):
        mock_plot_curves.return_value = 'mock_figure'
        result = self.converter.plot()
        self.assertEqual(result, 'mock_figure')

    @patch('crossreads_petrography.isotopes.IsotopeConverter.df_intersections', new_callable=PropertyMock)
    @patch('crossreads_petrography.isotopes.IsotopeConverter.plot')
    def test_save(self, mock_plot, mock_df_intersections):
        mock_df = pd.DataFrame({'Sample': ['ISic001', 'ISic002']})
        mock_df_intersections.return_value = mock_df
        mock_plot.return_value = 'mock_figure'
        
        with patch('pandas.DataFrame.to_excel') as mock_to_excel:
            self.converter.save()
            mock_to_excel.assert_called_once()
            mock_plot.assert_called_once()

class TestHelperFunctions(unittest.TestCase):
    def test_plot_curves(self):
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
        
        self.assertIsNotNone(result)
        # Add more specific assertions about the figure if needed

    def test_determine_polygon_intersections(self):
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
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertEqual(result.loc['ISic001', 'type1'], '✔️')
        self.assertEqual(result.loc['ISic002', 'type1'], '✖️')

if __name__ == '__main__':
    unittest.main()