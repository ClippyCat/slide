import random

# Define the grid size
GRID_SIZE = 2

# Function to print the current state of the puzzle
def print_puzzle(puzzle):
	for row in puzzle:
		print(" ".join(map(str, row)))

# Function to swap two tiles
def swap(puzzle, r1, c1, r2, c2):
	puzzle[r1][c1], puzzle[r2][c2] = puzzle[r2][c2], puzzle[r1][c1]

def is_solved(puzzle):
	n = 1
	for row in puzzle:
		for cell in row:
			if cell != n and n != GRID_SIZE ** 2:
				return False
			n+=1
	return True

# Function to generate a random solvable puzzle using recursion
def generate(puzzle, numbers):
	if not numbers:
		return puzzle
	random.shuffle(numbers)

	for i in range(GRID_SIZE):
		for j in range(GRID_SIZE):
			if i == GRID_SIZE - 1 and j == GRID_SIZE - 1:
				break
			puzzle[i][j] = numbers.pop()

	if is_solvable(puzzle):
		return puzzle
	else:
		return generate(puzzle, numbers)

# Function to generate a random solvable puzzle
def generate_random_puzzle():
	puzzle = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
	numbers = list(range(1, GRID_SIZE ** 2))
	return generate(puzzle, numbers)

# Function to count inversions
def count_inversions(puzzle):
    flat_puzzle = [cell for row in puzzle for cell in row if cell != 0]
    inversions = 0

    for i in range(len(flat_puzzle)):
        for j in range(i + 1, len(flat_puzzle)):
            if flat_puzzle[i] != 0 and flat_puzzle[j] != 0 and flat_puzzle[i] > flat_puzzle[j]:
                inversions += 1

    return inversions

# Function to check if a puzzle is solvable
def is_solvable(puzzle):
	inversions = count_inversions(puzzle)
	return inversions % 2 == 0

# Function to move a tile in the puzzle
def move(puzzle, direction):
	empty_row, empty_col = find_empty(puzzle)

	if direction == 'W' and empty_row < GRID_SIZE - 1:
		swap(puzzle, empty_row, empty_col, empty_row + 1, empty_col)
	elif direction == 'S' and empty_row > 0:
		swap(puzzle, empty_row, empty_col, empty_row - 1, empty_col)
	elif direction == 'A' and empty_col < GRID_SIZE - 1:
		swap(puzzle, empty_row, empty_col, empty_row, empty_col + 1)
	elif direction == 'D' and empty_col > 0:
		swap(puzzle, empty_row, empty_col, empty_row, empty_col - 1)

# Function to find the empty tile
def find_empty(puzzle):
	for i in range(GRID_SIZE):
		for j in range(GRID_SIZE):
			if puzzle[i][j] == 0:
				return i, j

# Main game loop
def main():
	puzzle = generate_random_puzzle()

	print(f"Welcome to the {GRID_SIZE}x{GRID_SIZE} Sliding Square Puzzle!")
	print("Use 'W' (up), 'A' (left), 'S' (down), and 'D' (right) to move the tiles.")
	print("To quit, press 'Q'.")

	while True:
		print_puzzle(puzzle)

		if is_solved(puzzle):
			print("Congratulations! You've solved the puzzle.")
			break

		move_direction = input("Enter a move (W/A/S/D): ").upper()

		if move_direction == 'Q':
			print("Quitting the game.")
			break
		elif move_direction in ['W', 'A', 'S', 'D']:
			move(puzzle, move_direction)
		else:
			print("Invalid move. Use 'W/A/S/D' to move the tiles or 'Q' to quit.")

if __name__ == "__main__":
	main()
