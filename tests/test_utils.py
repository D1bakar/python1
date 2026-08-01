import os
from numbergame import utils

def test_get_data_dir_creates_or_returns_path():
    path = utils.get_data_dir()
    assert os.path.isdir(path)
    assert path.endswith('.numbergame') or os.path.isdir(path)

def test_stats_path_ends_with_stats_json():
    p = utils.get_stats_path()
    assert p.endswith('stats.json')
