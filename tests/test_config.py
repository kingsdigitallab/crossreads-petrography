from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from crossreads_petrography import *


import pytest

@pytest.fixture
def sample_config():
    return Config.from_yaml(PATH_CONFIG_DEFAULT)

def test_from_yaml(sample_config):
    assert isinstance(sample_config, Config)
    assert len(sample_config) > 0

def test_flatten_dict():
    nested_dict = {
        'a': 1,
        'b': {
            'c': 2,
            'd': {
                'e': 3
            }
        }
    }
    flattened = Config.flatten_dict(nested_dict)
    assert flattened == {'a': 1, 'b.c': 2, 'b.d.e': 3}

def test_get_existing_key(sample_config):
    assert sample_config.get('paths.root.local') == str(Path(__file__).parent.parent / "data")

def test_get_nonexistent_key(sample_config):
    assert sample_config.get('nonexistent_key', 'default') == 'default'

def test_getitem_existing_key(sample_config):
    assert sample_config['paths.root.local'] == str(Path(__file__).parent.parent / "data")

def test_getitem_nonexistent_key(sample_config):
    with pytest.raises(KeyError):
        sample_config['nonexistent_key']

def test_paths_property(sample_config):
    paths = sample_config.paths
    assert isinstance(paths, dict)
    assert 'root' in paths
    assert 'data' in paths
    assert 'metadata' in paths

def test_get_path(sample_config):
    expected_local_path = str(Path(__file__).parent.parent / "data")
    expected_path = '/content/drive/MyDrive/Crossreads B D1/crossreads_petrography_data' if in_colab() else expected_local_path
    actual_path = sample_config.get_path('root')
    assert actual_path == expected_path, f"Actual path: {actual_path} does not match expected path: {expected_path}"

def test_df_property(sample_config):
    df = sample_config.df
    assert 'value' in df.columns
    assert len(df) > 0

def test_placeholder_expansion(sample_config):
    assert sample_config['paths.metadata.local'] == str(Path(__file__).parent.parent / "data" / "Metadata")

def test_colab_specific_value(sample_config):
    # Mocking in_colab() as True
    import crossreads_petrography.constants
    crossreads_petrography.constants.in_colab() = True
    
    assert sample_config.get('paths.root') == "/content/drive/MyDrive/Crossreads B D1/crossreads_petrography_data"

    # Reset in_colab() to False
    crossreads_petrography.constants.in_colab() = False
