import random
import os

# Clear the screen
os.system('cls' if os.name == 'nt' else 'clear')

# Welcome message and player input
print("Welcome to Battleship!")
player_name = input("Enter your name: ")

# Create empty 7x7 boards
player_board = [["~" for _ in range(7)] for _ in range(7)]
hidden_board = [["~" for _ in range(7)] for _ in range(7)]

# Ship sizes and positions
ships = {3: 1, 2: 2, 1: 4}
ship_positions = []

# Place ships on the hidden board
for size, count in ships.items():
    for _ in range(count):
        while True:
            x = random.randint(0, 6)
            y = random.randint(0, 6)
            direction = random.choice(["H", "V"])
            ship_cells = [(x + i, y) if direction == "H" else (x, y + i) for i in range(size)]
            valid = True

            for cell in ship_cells:
                cx, cy = cell
                if cx < 0 or cx >= 7 or cy < 0 or cy >= 7 or hidden_board[cx][cy] != "~":
                    valid = False
                    break
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < 7 and 0 <= ny < 7 and hidden_board[nx][ny] == "S":
                            valid = False

            if valid:
                for cx, cy in ship_cells:
                    hidden_board[cx][cy] = "S"
                ship_positions.append(ship_cells)
                break

# Game variables
hits = set()
attempts = 0

# Game loop
while True:
    # Clear the screen and print the player board
    os.system('cls' if os.name == 'nt' else 'clear')
    print("  A B C D E F G")
    for i, row in enumerate(player_board):
        print(f"{i + 1} " + " ".join(row))

    # Check if all ships are sunk
    all_sunk = all(all(cell in hits for cell in ship) for ship in ship_positions)
    if all_sunk:
        print("Congratulations! You sank all the ships!")
        print(f"It took you {attempts} shots.")
        break

    # Get user input for the shot
    coord = input("Enter your shot (e.g., B5): ").upper()
    if len(coord) != 2 or coord[0] not in "ABCDEFG" or coord[1] not in "1234567":
        print("Invalid input. Try again.")
        input("Press Enter to continue...")
        continue

    x = int(coord[1]) - 1
    y = ord(coord[0]) - ord("A")

    # Check if the cell was already shot at
    if player_board[x][y] in ("M", "H"):
        print("You already shot here. Try again.")
        input("Press Enter to continue...")
        continue

    # Process the shot
    attempts += 1
    if hidden_board[x][y] == "S":
        player_board[x][y] = "H"
        hits.add((x, y))
        print("Hit!")
        # Check if a ship is sunk
        for ship in ship_positions:
            if all(cell in hits for cell in ship):
                print("You sunk a ship!")
    else:
        player_board[x][y] = "M"
        print("Miss!")

    input("Press Enter to continue...")

# End game
print("Thanks for playing Battleship!")