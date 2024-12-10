import pandas as pd
import numpy as np
from crossreads_petrography import MgsConverter, XRDConverter
import pytest

class TestMGSIntegration:
    @pytest.fixture
    def mgs(self):
        return MgsConverter()

    # def test_specific_sample_intersections(self, mgs):
    #     result = mgs.df_output

    #     assert 'ISic000097' in result.index, "ISic000097 not found in the results"

    #     # Optical microscopy tests (1.4mm)
    #     assert '🔬🔬' in result.loc['ISic000097', 'Aphrodisias'], "ISic000097 optical does not fully intersect with Aphrodisias"
    #     assert '🔬🔬' in result.loc['ISic000097', 'Docimium'], "ISic000097 optical does not fully intersect with Docimium"
    #     assert '🔬🔬' in result.loc['ISic000097', 'Paros-1'], "ISic000097 optical does not fully intersect with Paros-1"
    #     assert '🔬🔬' in result.loc['ISic000097', 'Paros-2 (3)'], "ISic000097 optical does not fully intersect with Paros-2 (3)"
    #     assert '🔬🔬' in result.loc['ISic000097', 'Paros-4'], "ISic000097 optical does not fully intersect with Paros-4"
    #     assert '🔬' in result.loc['ISic000097', 'Göktepe'], "ISic000097 optical does not intersect with Göktepe whisker"
    #     assert '🔬' in result.loc['ISic000097', 'Proconnesos-1'], "ISic000097 optical does not intersect with Proconnesos-1 whisker"
    #     assert '🔬' in result.loc['ISic000097', 'Pentelikon'], "ISic000097 optical does not intersect with Pentelikon whisker"
    #     assert '🔬' in result.loc['ISic000097', 'Thasos-3'], "ISic000097 optical does not intersect with Thasos-3 whisker"

    #     # Digital microscopy tests (2mm)
    #     assert '🔍🔍' in result.loc['ISic000097', 'Aphrodisias'], "ISic000097 digital does not fully intersect with Aphrodisias"
    #     assert '🔍🔍' in result.loc['ISic000097', 'Proconnesos-1'], "ISic000097 digital does not fully intersect with Proconnesos-1"
    #     assert '🔍🔍' in result.loc['ISic000097', 'Paros-1'], "ISic000097 digital does not fully intersect with Paros-1"
    #     assert '🔍🔍' in result.loc['ISic000097', 'Paros-2 (3)'], "ISic000097 digital does not fully intersect with Paros-2 (3)"
    #     assert '🔍🔍' in result.loc['ISic000097', 'Paros-4'], "ISic000097 digital does not fully intersect with Paros-4"
    #     assert '🔍🔍' in result.loc['ISic000097', 'Thasos-3'], "ISic000097 digital does not fully intersect with Thasos-3"
    #     assert '🔍' in result.loc['ISic000097', 'Docimium'], "ISic000097 digital does not intersect with Docimium whisker"
    #     assert '🔍' in result.loc['ISic000097', 'Naxos'], "ISic000097 digital does not intersect with Naxos whisker"
    #     assert '🔍' in result.loc['ISic000097', 'Thasos-1 (2)'], "ISic000097 digital does not intersect with Thasos-1 (2) whisker"

    #     # Print ranges and values for debugging
    #     print(f"ISic000097 optical value: {mgs.df_microscopy.loc['ISic000097', mgs.col_optical]}")
    #     print(f"ISic000097 digital value: {mgs.df_microscopy.loc['ISic000097', mgs.col_digital]}")
    #     for marble_type in result.columns:
    #         print(f"ISic000097 {marble_type} result: {result.loc['ISic000097', marble_type]}")
    #         print(f"{marble_type} whisker range: {mgs.df_ranges.loc[marble_type, 'wh_min']} - {mgs.df_ranges.loc[marble_type, 'wh_max']}")
    #         print(f"{marble_type} box range: {mgs.df_ranges.loc[marble_type, 'box_min']} - {mgs.df_ranges.loc[marble_type, 'box_max']}")


    def test_not_too_many_symbols(self, mgs):
        for i,row in mgs.df_output.iterrows():
            for k,v in row.items():
                assert type(v) is str, 'Not string value'
                assert v.count('🔍')<=2, 'Too many symbols'
                assert v.count('🔬')<=2, 'Too many symbols'

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

    

class TestXRDIntegration:
    @pytest.fixture
    def xrd(self):
        return XRDConverter()
    
    def test_xrd_data_for_ISic000097(self, xrd):
        result = xrd.df_output
        isic = 'ISic000097p'

        assert isic in result.index, f"{isic} not found in the XRD results"
        # Check individual mineral contents
        assert round(result.loc[isic, 'XRD calcite content (%)']) == 97
        assert round(result.loc[isic, 'XRD dolomite content (%)']) == 3


