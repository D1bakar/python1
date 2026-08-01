import os

STATS_FILENAME = "stats.json"
LEADERBOARD_FILENAME = "leaderboard.json"
DATA_DIRNAME = ".numbergame"

def get_data_dir():
    """Return a path to the user data directory for the game and ensure it exists.

    By default we use ~/.numbergame so the files are user-writable and persist
    across installs/updates.
    """
    home = os.path.expanduser("~")
    data_dir = os.path.join(home, DATA_DIRNAME)
    try:
        os.makedirs(data_dir, exist_ok=True)
    except Exception:
        # Fall back to package directory if we can't create the home dir
        data_dir = os.path.abspath(os.path.dirname(__file__))
    return data_dir

def get_stats_path():
    """Return the path to the stats file in the user data directory."""
    return os.path.join(get_data_dir(), STATS_FILENAME)

def get_leaderboard_path():
    """Return the path to the leaderboard file in the user data directory."""
    return os.path.join(get_data_dir(), LEADERBOARD_FILENAME)
