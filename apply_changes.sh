#!/usr/bin/env bash
set -euo pipefail

# Ensure directories exist
mkdir -p numbergame
mkdir -p .github/workflows
mkdir -p tests

# numbergame/__init__.py
cat > numbergame/__init__.py <<'PY'
"""Number Guessing Game package modules.

This package contains small modules to keep code organized:
- game.py: contains Game class and gameplay logic
- stats.py: load/save stats to JSON
- ui.py: user input and display helpers
- utils.py: filesystem helpers
"""
PY

# numbergame/utils.py
cat > numbergame/utils.py <<'PY'
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
PY

# numbergame/stats.py
cat > numbergame/stats.py <<'PY'
import json
from .utils import get_stats_path

def load_stats():
    """Load statistics from a JSON file. Return default stats if file missing/invalid."""
    path = get_stats_path()
    default = {"games": 0, "wins": 0, "total_attempts": 0, "best_score": None}

    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)

        # Validate and normalize loaded data
        stats = {
            "games": int(data.get("games", 0)),
            "wins": int(data.get("wins", 0)),
            "total_attempts": int(data.get("total_attempts", 0)),
            "best_score": data.get("best_score", None),
        }

        if isinstance(stats["best_score"], (int, float)):
            stats["best_score"] = int(stats["best_score"]) if stats["best_score"] != float("inf") else None
        else:
            stats["best_score"] = None

        return stats

    except FileNotFoundError:
        return default
    except (json.JSONDecodeError, ValueError):
        print("Warning: stats file is corrupted or invalid. Starting with fresh statistics.")
        return default
    except Exception as e:
        print(f"Warning: failed to load stats ({e}). Starting with fresh statistics.")
        return default

def save_stats(stats):
    """Save statistics to a JSON file in the user data directory."""
    path = get_stats_path()
    data = stats.copy()

    # JSON can't represent inf; store None when best_score is not set
    if data.get("best_score") is None:
        data["best_score"] = None

    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=4)
    except Exception as e:
        print(f"Warning: failed to save stats ({e}).")
PY

# numbergame/leaderboard.py
cat > numbergame/leaderboard.py <<'PY'
import json
from .utils import get_leaderboard_path

DEFAULT_LEADERBOARD = []

def load_leaderboard():
    """Load leaderboard from JSON file or return default empty list."""
    path = get_leaderboard_path()
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            if isinstance(data, list):
                # ensure each entry has expected keys
                cleaned = []
                for item in data:
                    name = item.get("name") if isinstance(item, dict) else None
                    score = item.get("score") if isinstance(item, dict) else None
                    if name and isinstance(score, int):
                        cleaned.append({"name": str(name), "score": int(score)})
                return cleaned
    except FileNotFoundError:
        return DEFAULT_LEADERBOARD
    except Exception:
        return DEFAULT_LEADERBOARD

    return DEFAULT_LEADERBOARD

def save_leaderboard(board):
    """Save leaderboard list to JSON file."""
    path = get_leaderboard_path()
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(board, fh, indent=4)
    except Exception as e:
        print(f"Warning: failed to save leaderboard ({e}).")

def update_leaderboard(name: str, score: int, top_n: int = 10):
    """Add or update an entry for name with the (lower is better) score.

    Keeps only the top_n best (lowest) scores.
    """
    if not name:
        return

    board = load_leaderboard()

    # If player exists and new score is better, update it; otherwise add if new
    found = False
    for entry in board:
        if entry["name"] == name:
            found = True
            if score < entry["score"]:
                entry["score"] = score
            break

    if not found:
        board.append({"name": name, "score": score})

    # sort by score ascending (lower is better)
    board.sort(key=lambda e: e["score"]) 

    # keep top_n
    board = board[:top_n]

    save_leaderboard(board)

def format_leaderboard(board=None):
    if board is None:
        board = load_leaderboard()

    if not board:
        return "\nNo entries in the leaderboard yet."

    lines = ["\nLEADERBOARD (Top {})".format(len(board)), "=" * 30]
    for idx, entry in enumerate(board, start=1):
        lines.append(f"{idx}. {entry['name']}: {entry['score']} attempts")
    return "\n".join(lines)
PY

# numbergame/ui.py
cat > numbergame/ui.py <<'PY'
def get_int_input(prompt, min_value=None, max_value=None):
    """Ask the user for an integer, optionally enforcing a min/max range."""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Please enter a number >= {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Please enter a number <= {max_value}.")
                continue
            return value
        except ValueError:
            print("Invalid input! Please enter a valid integer.")

def get_difficulty():
    """Get difficulty level from user and return (max_number, max_attempts)."""
    while True:
        print("\nSelect Difficulty Level:")
        print("1. Easy (1-50, 15 attempts)")
        print("2. Medium (1-100, 10 attempts)")
        print("3. Hard (1-200, 7 attempts)")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            return 50, 15
        elif choice == "2":
            return 100, 10
        elif choice == "3":
            return 200, 7
        else:
            print("Invalid choice. Please try again.")

def display_stats(stats):
    """Display overall statistics in a readable format."""
    if not stats["games"]:
        print("\nNo games played yet!")
        return

    avg_attempts = stats["total_attempts"] / stats["games"]
    win_rate = (stats["wins"] / stats["games"]) * 100

    best_score = stats.get("best_score")
    best_display = f"{best_score} attempts" if best_score is not None else "N/A"

    print("\n" + "=" * 40)
    print("GAME STATISTICS")
    print("=" * 40)
    print(f"Total Games Played: {stats['games']}")
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['games'] - stats['wins']}")
    print(f"Win Rate: {win_rate:.1f}%")
    print(f"Average Attempts: {avg_attempts:.1f}")
    print(f"Best Score: {best_display}")
    print("=" * 40)

def print_menu():
    print("\nMAIN MENU")
    print("1. Play Game")
    print("2. View Statistics & Leaderboard")
    print("3. Exit")
PY

# numbergame/game.py
cat > numbergame/game.py <<'PY'
import random
from .ui import get_int_input

class Game:
    """Encapsulates a single number-guessing game instance.

    Features:
    - Warmer/Colder hinting compared to previous guess
    - Input validation through ui.get_int_input
    """

    def __init__(self, max_number: int, max_attempts: int):
        self.max_number = max_number
        self.max_attempts = max_attempts
        self.secret = random.randint(1, max_number)

    def play(self):
        attempts = 0
        prev_distance = None

        print(f"\nI'm thinking of a number between 1 and {self.max_number}.")
        print(f"You have {self.max_attempts} attempts to guess it!\n")

        while attempts < self.max_attempts:
            guess = get_int_input(f"Attempt {attempts + 1}/{self.max_attempts} - Enter your guess: ", 1, self.max_number)

            attempts += 1

            if guess == self.secret:
                print(f"\n🎉 Congratulations! You guessed the number in {attempts} attempts!")
                return True, attempts

            # Provide feedback and a warmer/colder style hint
            distance = abs(self.secret - guess)
            if guess < self.secret:
                direction = "Too low"
            else:
                direction = "Too high"

            hint = ""
            if prev_distance is not None:
                if distance < prev_distance:
                    hint = " Getting warmer! 🔥"
                elif distance > prev_distance:
                    hint = " Getting colder. 🧊"
                else:
                    hint = " Same distance as before."

            remaining = self.max_attempts - attempts
            print(f"{direction}!{hint} ({remaining} attempts left)")

            prev_distance = distance

        print(f"\n❌ Game Over! The number was {self.secret}.")
        return False, attempts
PY

# numbergame/difficulties.json
cat > numbergame/difficulties.json <<'PY'
{
  "easy": {"max_number": 50, "attempts": 15},
  "medium": {"max_number": 100, "attempts": 10},
  "hard": {"max_number": 200, "attempts": 7}
}
PY

# main.py
cat > main.py <<'PY'
# Top-level CLI that wires the package together
from numbergame import game as _game_module
from numbergame.stats import load_stats, save_stats
from numbergame.ui import get_difficulty, display_stats, print_menu
from numbergame import leaderboard as lb

def main():
    print("\n" + "=" * 40)
    print("WELCOME TO NUMBER GUESSING GAME!")
    print("=" * 40)

    stats = load_stats()

    player_name = input("\nEnter your player name (leave empty for 'Player'): ").strip() or "Player"

    while True:
        print_menu()

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            max_number, max_attempts = get_difficulty()
            game = _game_module.Game(max_number, max_attempts)
            won, attempts = game.play()

            stats["games"] += 1
            stats["total_attempts"] += attempts

            if won:
                stats["wins"] += 1
                if stats.get("best_score") is None or attempts < stats.get("best_score"):
                    stats["best_score"] = attempts

                # Update per-player leaderboard
                lb.update_leaderboard(player_name, attempts)

            # Save after each completed game so progress persists
            save_stats(stats)

        elif choice == "2":
            display_stats(stats)
            print(lb.format_leaderboard())

        elif choice == "3":
            save_stats(stats)
            print("\nThanks for playing! Goodbye! 👋")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
PY

# pyproject.toml
cat > pyproject.toml <<'PY'
[tool.poetry]
name = "numbergame"
version = "0.1.0"
description = "A small modular number guessing game"

[tool.poetry.dependencies]
python = "^3.8"

[tool.poetry.dev-dependencies]
pytest = "^7.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
PY

# .github/workflows/ci.yml
cat > .github/workflows/ci.yml <<'PY'
name: Python package
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest
    - name: Run tests
      run: |
        pytest -q
PY

# tests/test_utils.py
cat > tests/test_utils.py <<'PY'
import os
from numbergame import utils

def test_get_data_dir_creates_or_returns_path():
    path = utils.get_data_dir()
    assert os.path.isdir(path)
    assert path.endswith('.numbergame') or os.path.isdir(path)

def test_stats_path_ends_with_stats_json():
    p = utils.get_stats_path()
    assert p.endswith('stats.json')
PY

# tests/test_leaderboard.py
cat > tests/test_leaderboard.py <<'PY'
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
PY

# README.md
cat > README.md <<'PY'
# Number Guessing Game

This repository is a modular number guessing game written in Python.

New features added:
- Per-player leaderboard (stored in ~/.numbergame/leaderboard.json)
- Stats and leaderboard stored in user data dir (~/.numbergame)
- Difficulty presets file (numbergame/difficulties.json)
- Unit test skeleton using pytest (tests/)
- GitHub Actions workflow to run tests (.github/workflows/ci.yml)
- pyproject.toml (Poetry format) for packaging and dev deps

Run locally:
- python main.py
- Run tests: pytest
PY

echo "All files created. Please git add, commit, and push from your account."
