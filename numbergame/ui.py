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
    print("2. View Statistics")
    print("3. Exit")
