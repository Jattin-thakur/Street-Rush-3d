import random
a = random.randint(1,1000)
try:
    guess = int(input("Guess the number between 1 and 1000: "))
    if guess < 1 or guess > 1000:
        raise ValueError("Guess must be between 1 and 1000.")
    if guess < a:
        print("Too low! Try again.")
    elif guess > a:
        print("Too high! Try again.")
    else:
        print("Congratulations! You guessed the correct number.")
except ValueError as ve:
    print(f"Invalid input: {ve}")