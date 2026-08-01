import random
import json
import os

STATS_FILENAME = "stats.json"


def get_stats_path():
    """Return the path to the stats file next to this script."""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_dir, STATS_FILENAME)


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

        # If best_score was stored as a number, ensure it's an int; if inf or invalid, set to None
        if isinstance(stats["best_score"], (int, float)):
            stats["best_score"] = (
                int(stats["best_score"])
                if stats["best_score"] != float("inf")
                else None
            )
        else:
            stats["best_score"] = None

        return stats

    except FileNotFoundError:
        return default
    except (json.JSONDecodeError, ValueError):
        print(
            "Warning: stats file is corrupted or invalid. Starting with fresh statistics."
        )
        return default
    except Exception as e:
        print(f"Warning: failed to load stats ({e}). Starting with fresh statistics.")
        return default


def save_stats(stats):
    """Save statistics to a JSON file next to this script."""
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


def get_difficulty():
    """Get difficulty level from user."""
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
    """Display overall statistics."""
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


def play_game(max_number, max_attempts):
    """Play a single round of the guessing game."""
    number = random.randint(1, max_number)
    attempts = 0

    print(f"\nI'm thinking of a number between 1 and {max_number}.")
    print(f"You have {max_attempts} attempts to guess it!\n")

    while attempts < max_attempts:
        try:
            guess = int(
                input(f"Attempt {attempts + 1}/{max_attempts} - Enter your guess: ")
            )

            if guess < 1 or guess > max_number:
                print(f"Please enter a number between 1 and {max_number}.")
                continue

            attempts += 1

            if guess < number:
                remaining = max_attempts - attempts
                print(f"Too low! Try again. ({remaining} attempts left)")
            elif guess > number:
                remaining = max_attempts - attempts
                print(f"Too high! Try again. ({remaining} attempts left)")
            else:
                print(
                    f"\n🎉 Congratulations! You guessed the number in {attempts} attempts!"
                )
                return True, attempts

        except ValueError:
            print("Invalid input! Please enter a valid number.")

    print(f"\n❌ Game Over! The number was {number}.")
    return False, attempts
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
                if stats.get("best_score") is None or attempts < stats.get(
                    "best_score"
                ):
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
