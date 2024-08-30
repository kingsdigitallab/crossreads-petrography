import pandas as pd
import numpy as np
from crossreads_petrography import MgsConverter

import pytest
import pandas as pd
import numpy as np
from crossreads_petrography import MgsConverter

class TestMGSIntegration:
    @pytest.fixture
    def mgs(self):
        return MgsConverter()

    def test_specific_sample_intersections(self, mgs):
        result = mgs.df_output

        assert 'ISic000097' in result.index, "ISic000097 not found in the results"

        assert '🔬🔬' in result.loc['ISic000097', 'Docimium'], "ISic000097 optical does not fully intersect with Docimium"
        assert '🔍' in result.loc['ISic000097', 'Docimium'], "ISic000097 digital does not intersect with Docimium whisker"
        assert '🔍🔍' not in result.loc['ISic000097', 'Docimium'], "ISic000097 digital should not fully intersect with Docimium"

        assert '🔬🔬' in result.loc['ISic000097', 'Paros-1'], "ISic000097 optical does not fully intersect with Paros-1"
        assert '🔍🔍' in result.loc['ISic000097', 'Paros-1'], "ISic000097 digital does not fully intersect with Paros-1"

        # Print ranges and values for debugging
        print(f"Docimium whisker range: {mgs.df_ranges.loc['Docimium', 'wh_min']} - {mgs.df_ranges.loc['Docimium', 'wh_max']}")
        print(f"Docimium box range: {mgs.df_ranges.loc['Docimium', 'box_min']} - {mgs.df_ranges.loc['Docimium', 'box_max']}")
        print(f"Paros-1 whisker range: {mgs.df_ranges.loc['Paros-1', 'wh_min']} - {mgs.df_ranges.loc['Paros-1', 'wh_max']}")
        print(f"Paros-1 box range: {mgs.df_ranges.loc['Paros-1', 'box_min']} - {mgs.df_ranges.loc['Paros-1', 'box_max']}")
        print(f"ISic000097 optical value: {mgs.df_microscopy.loc['ISic000097', mgs.col_optical]}")
        print(f"ISic000097 digital value: {mgs.df_microscopy.loc['ISic000097', mgs.col_digital]}")
        print(f"ISic000097 Docimium result: {result.loc['ISic000097', 'Docimium']}")
        print(f"ISic000097 Paros-1 result: {result.loc['ISic000097', 'Paros-1']}")

    def test_multiple_samples(self, mgs):
        result = mgs.df_output

        samples_to_test = ['ISic000104', 'ISic000121', 'ISic000148']
        for sample in samples_to_test:
            assert sample in result.index, f"{sample} not found in the results"
            # Add more specific assertions for each sample as needed

    def test_dataframe_structure(self, mgs):
        result = mgs.df_output

        expected_columns = ['Aphrodisias', 'Carrara', 'Docimium', 'Göktepe', 'Hymettus', 'Naxos',
                            'Paros-1', 'Paros-2 (3)', 'Paros-4', 'Pentelikon', 'Proconnesos-1',
                            'Thasos-1 (2)', 'Thasos-3']
        assert set(expected_columns) - set(result.columns) == set(), "Columns in the result do not match expected columns"

        expected_row_count = 33  # Replace with the actual expected number of rows
        assert len(result) == expected_row_count, f"Expected {expected_row_count} rows, but got {len(result)}"

    # Add more integration tests as needed