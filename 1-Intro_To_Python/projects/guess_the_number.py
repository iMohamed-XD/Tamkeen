import random

levels = {
    "easy": {
        "range": 50,
        "attempts": 10,
    },
    "medium": {
        "range": 100,
        "attempts": 7,
    },
    "hard": {
        "range": 500,
        "attempts": 5,
    }
}
def main():
    failed = True
    print("====Welcome to Guess the Number Game====")
    diffeculty = input("enter the diffculty {easy (1 -> 50), medium (1 -> 100), hard (1 -> 500)}\n")
    if diffeculty not in levels:
        print("invalid diffeculty, choose from {easy, medium, hard}")
        return
    computer_choice = random.choice(range(levels[diffeculty]["range"])) #from 1 to the chosen limit
    rounds = 0
    for _ in range(levels[diffeculty]["attempts"]):
        user_choice = int(input(f"the computer choose randomly between 1 and {levels[diffeculty]['range']}, guess the number!\n"))
        if user_choice < 1 or user_choice > levels[diffeculty]["range"]:
            print(f"invalid number, choose between 1 and {levels[diffeculty]['range']}")
            continue

        if computer_choice == user_choice:
            print(f"you guessed correctly!!, number = {computer_choice}, rounds = {rounds + 1}")
            failed = False
            break
        elif computer_choice > user_choice:
            rounds += 1
            print("TOO Low, try again")
        elif computer_choice < user_choice:
            rounds += 1
            print("TOO High, try again")
    if failed:
        print(f"you failed to guess the number, it was {computer_choice}")


if __name__ == "__main__":
    main()
