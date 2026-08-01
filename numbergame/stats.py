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
