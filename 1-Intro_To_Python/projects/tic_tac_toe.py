import random

GRID = [i + 1 for i in range(9)]  # Initialize a 3x3 grid with empty spaces
WINNING_COMBINATIONS = [
    (2,1,0),
    (5,4,3),
    (8,7,6),
    (6,3,0),
    (7,4,1),
    (8,5,2),
    (8,4,0),
    (6,4,2),
]
modes = (1, 2)
x_wins = 0
o_wins = 0
draws = 0
def check_winner(GRID: list):
    for combination in WINNING_COMBINATIONS:
        if GRID[combination[0]] == GRID[combination[1]] == GRID[combination[2]] and GRID[combination[0]] in ["X", "O"]:
            return GRID[combination[0]]

def print_grid():
    print(f"{GRID[0]} | {GRID[1]} | {GRID[2]}")
    print("--+---+--")
    print(f"{GRID[3]} | {GRID[4]} | {GRID[5]}")
    print("--+---+--")
    print(f"{GRID[6]} | {GRID[7]} | {GRID[8]}")

def main():
    global x_wins, o_wins, draws
    global draw
    draw = True

    print("Welcome to Tic Tac Toe!")
    mode = int(input("choose the mode: \n1. Player VS Player\n2. Player VS Computer\n"))
    if mode not in modes:
        print("Invalid choice!!!")
        return

    o_turn = False
    for _ in range(9):
        print_grid()
        if not o_turn:
            print("PLAYER X Turn!")
            x_choice = int(input("enter the Tile number\n")) - 1
            if x_choice < 0 or x_choice > 9:
                print("Invalid choice!!!")
                continue
            if GRID[x_choice] == "O":
                print("This Tile is already taken!!")
                continue
            GRID[x_choice] = "X"
            o_turn = True
        else:
            if mode == 1:
                print("PLAYER O Turn!")
                o_choice = int(input("enter the Tile number\n")) - 1
                if o_choice < 0 or o_choice > 9:
                    print("Invalid choice!!!")
                    continue
                if GRID[o_choice] == "X":
                    print("This Tile is already taken!!")
                    continue
                GRID[o_choice] = "O"
                o_turn = False
            else:
                print("PLAYER O Turn!")
                o_choice = int(random.choice(range(1, 10))) - 1
                if GRID[o_choice] == "X":
                    continue
                GRID[o_choice] = "O"
                print(f"Computer choose Tile number {o_choice}")
                o_turn = False

        winner = check_winner(GRID=GRID)
        if winner == "X":
            x_wins += 1
            draw = False
            print(f"Player {winner} Has WON!!!")
            break
        elif winner == "O":
            o_wins += 1
            draw = False
            print(f"Player {winner} has WON!!!")
            break
        else:
            continue
    if draw:
        draws += 1
        print("It's a Draw!!!")

if __name__ == "__main__":
    while True:
        main()
        print(f"X wins: {x_wins}, O wins: {o_wins}, Draws: {draws}")
        print_grid()
        choice = input("Do you want to play again? (y/n): ")
        if choice.lower() != "y":
            break
