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
