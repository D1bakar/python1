import os
from numbergame import leaderboard
from numbergame.utils import get_leaderboard_path
from pathlib import Path

def test_leaderboard_roundtrip(tmp_path, monkeypatch):
    # Redirect data dir to a temp directory
    monkeypatch.setenv('HOME', str(tmp_path))
    # ensure no leaderboard exists
    lp = get_leaderboard_path()
    if os.path.exists(lp):
        os.unlink(lp)

    leaderboard.update_leaderboard('Alice', 5)
    leaderboard.update_leaderboard('Bob', 7)
    board = leaderboard.load_leaderboard()
    assert any(e['name'] == 'Alice' for e in board)
    assert any(e['name'] == 'Bob' for e in board)

    # updating with better score should replace
    leaderboard.update_leaderboard('Bob', 4)
    board = leaderboard.load_leaderboard()
    bob = next(e for e in board if e['name'] == 'Bob')
    assert bob['score'] == 4
