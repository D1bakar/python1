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
