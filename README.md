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
