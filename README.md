# Number Guessing Game

This repository is a small, modular number guessing game written in Python.

Structure:
- numbergame/ - package containing game logic, UI helpers, and stats management
  - game.py      - Game class and gameplay logic
  - stats.py     - load/save stats to JSON
  - ui.py        - input and display helpers
  - utils.py     - filesystem helpers (where stats.json is located)
- main.py        - top-level CLI that uses the package

What's next:
- Want additional features? I can add: difficulty presets file, a leaderboard, unit tests, a GUI, or networked multiplayer.
