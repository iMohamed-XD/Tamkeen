import random


def main():
    print("Welcome to Rock Paper Scissors Game")
    CHOICES = ("rock", "paper", "scissors")
    rounds = int(input("How many rounds?\n"))
    user_points = 0
    computer_points = 0
    for _ in range(rounds):
        user_choice = input("chooce one from {rock, paper, scissors}\n").lower()
        if user_choice not in CHOICES:
            print("Invalid choice, choose from {rock, paper, scissors}")
            continue

        computer_choice = random.choice(CHOICES)
        print(f"Computer choose {computer_choice}")

        wins_agianst = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper",
        }

        if user_choice == computer_choice:
            print(f"DRAW!!, both choose {user_choice}")
        elif wins_agianst[user_choice] == computer_choice:
            user_points += 1
            print("YOU WIN!!!!")
        else:
            computer_points += 1
            print("COMPUTER WINS!!!")
        print(f"Your points = {user_points}, \n computer points = {computer_points}")
    print("\n\n== GAME OVER ==")
    if user_points > computer_points:
        print("YOU ARE THE WINNER!!!")
    elif user_points < computer_points:
        print("COMPUTER IS THE WINNER!!!")
    else:
        print("IT'S A DRAW!!!")

if __name__ == "__main__":
    main()
    while True:
        choice = input("Do you want to play again? (y/n): ")
        if choice.lower() == "y":
            main()
        elif choice.lower() == "n":
            print("Thanks for playing!")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")