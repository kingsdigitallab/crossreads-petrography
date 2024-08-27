import pytest
from pathlib import Path
from crossreads_petrography import *

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
    assert sample_config.get_path('root') == str(Path(__file__).parent.parent / "data")
    assert sample_config.get_path('nonexistent', 'default') == 'default'

def test_df_property(sample_config):
    df = sample_config.df
    assert 'value' in df.columns
    assert len(df) > 0

def test_placeholder_expansion(sample_config):
    assert sample_config['paths.metadata.local'] == str(Path(__file__).parent.parent / "data" / "Metadata")

def test_colab_specific_value(sample_config):
    # Mocking IN_COLAB as True
    import crossreads_petrography.constants
    crossreads_petrography.constants.IN_COLAB = True
    
    assert sample_config.get('paths.root') == "/content/drive/MyDrive/Crossreads B D1/crossreads_petrography_data"

    # Reset IN_COLAB to False
    crossreads_petrography.constants.IN_COLAB = False
