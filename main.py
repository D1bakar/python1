import random

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
    
    print("\n" + "="*40)
    print("GAME STATISTICS")
    print("="*40)
    print(f"Total Games Played: {stats['games']}")
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['games'] - stats['wins']}")
    print(f"Win Rate: {win_rate:.1f}%")
    print(f"Average Attempts: {avg_attempts:.1f}")
    print(f"Best Score: {stats['best_score']} attempts")
    print("="*40)

def play_game(max_number, max_attempts):
    """Play a single round of the guessing game."""
    number = random.randint(1, max_number)
    attempts = 0
    
    print(f"\nI'm thinking of a number between 1 and {max_number}.")
    print(f"You have {max_attempts} attempts to guess it!\n")
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts} - Enter your guess: "))
            
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
                print(f"\n🎉 Congratulations! You guessed the number in {attempts} attempts!")
                return True, attempts
        
        except ValueError:
            print("Invalid input! Please enter a valid number.")
    
    print(f"\n❌ Game Over! The number was {number}.")
    return False, attempts

def main():
    print("\n" + "="*40)
    print("WELCOME TO NUMBER GUESSING GAME!")
    print("="*40)
    
    stats = {
        "games": 0,
        "wins": 0,
        "total_attempts": 0,
        "best_score": float('inf')
    }
    
    while True:
        print("\nMAIN MENU")
        print("1. Play Game")
        print("2. View Statistics")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            max_number, max_attempts = get_difficulty()
            won, attempts = play_game(max_number, max_attempts)
            
            stats["games"] += 1
            stats["total_attempts"] += attempts
            
            if won:
                stats["wins"] += 1
                stats["best_score"] = min(stats["best_score"], attempts)
        
        elif choice == "2":
            display_stats(stats)
        
        elif choice == "3":
            print("\nThanks for playing! Goodbye! 👋")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
