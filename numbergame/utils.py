import os

STATS_FILENAME = "stats.json"


def get_stats_path():
    """Return the path to the stats file located next to this package module.

    Stats file will be stored inside the `numbergame` package directory so it
    travels with the game code and is easy to find.
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_dir, STATS_FILENAME)
