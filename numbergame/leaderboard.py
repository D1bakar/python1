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
