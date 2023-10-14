import random
import heapq

GRID_SIZE = int(input("Enter grid size:"))

# Function to print the current state of the puzzle
def print_puzzle(puzzle):
	for row in puzzle:
		print(" ".join(map(str, row)))

def is_solved(puzzle):
	n = 1
	for row in puzzle:
		for cell in row:
			if cell != n and n != GRID_SIZE ** 2:
				return False
			n+=1
	return True

# Function to generate a random solvable puzzle
def generate(puzzle, numbers):
	if numbers:
		random.shuffle(numbers)
		for i in range(GRID_SIZE):
			for j in range(GRID_SIZE):
				if i == GRID_SIZE - 1 and j == GRID_SIZE - 1:
					break
				puzzle[i][j] = numbers.pop()

	if is_solvable(puzzle):
		return puzzle
	return generate(puzzle, numbers)

# Function to generate a random solvable puzzle
def generate_random_puzzle():
	puzzle = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
	numbers = list(range(1, GRID_SIZE ** 2))
	return generate(puzzle, numbers)

# Function to check if a puzzle is solvable
def is_solvable(puzzle):
	if solve_puzzle(puzzle) == None:
		return False
	return True

# Function to swap two tiles
def swap(puzzle, r1, c1, r2, c2):
	puzzle[r1][c1], puzzle[r2][c2] = puzzle[r2][c2], puzzle[r1][c1]

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

# Function to solve the puzzle using A* algorithm
def solve_puzzle(puzzle):
	def h(state):
		# The heuristic function - in this case, we will use the Manhattan distance
		total_distance = 0
		for i in range(GRID_SIZE):
			for j in range(GRID_SIZE):
				if puzzle[i][j] != 0:
					target_row, target_col = divmod(puzzle[i][j] - 1, GRID_SIZE)
					total_distance += abs(i - target_row) + abs(j - target_col)
		return total_distance

	def is_valid(x, y):
		return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE

	start_state = [row[:] for row in puzzle]
	goal_state = [[i * GRID_SIZE + j + 1 for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
	goal_state[GRID_SIZE - 1][GRID_SIZE - 1] = 0

	open_list = [(h(start_state), 0, start_state)]
	closed_set = set()
	g_values = {tuple(map(tuple, start_state)): 0}

	while open_list:
		f, g, current_state = heapq.heappop(open_list)
		if current_state == goal_state:
			return g  # Return the number of moves to reach the goal state

		if tuple(map(tuple, current_state)) in closed_set:
			continue

		closed_set.add(tuple(map(tuple, current_state)))

		for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
			empty_row, empty_col = find_empty(current_state)
			new_row, new_col = empty_row + dx, empty_col + dy
			if is_valid(new_row, new_col):
				new_state = [row[:] for row in current_state]
				new_state[empty_row][empty_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[empty_row][empty_col]
				tentative_g = g_values[tuple(map(tuple, current_state))] + 1
				if tentative_g < g_values.get(tuple(map(tuple, new_state)), float('inf')):
					g_values[tuple(map(tuple, new_state))] = tentative_g
					heapq.heappush(open_list, (tentative_g + h(new_state), tentative_g, new_state))
	return None

# Main game loop
def main():

	puzzle = generate_random_puzzle()

	print(f"Welcome to the {GRID_SIZE}x{GRID_SIZE} Sliding Square Puzzle!")
	print(f"You could solve the puzzle in {solve_puzzle(puzzle)} moves")
	print("Use 'W' (up), 'A' (left), 'S' (down), and 'D' (right) to move the tiles.")
	print("To quit, press 'Q'.")

	moves = 0
	while True:
		print_puzzle(puzzle)

		if is_solved(puzzle):
			print(f"Congratulations! You've solved the puzzle in {moves} moves!")
			break

		move_direction = input("Enter a move (W/A/S/D): ").upper()

		if move_direction == 'Q':
			print("Quitting the game.")
			break
		elif move_direction in ['W', 'A', 'S', 'D']:
			move(puzzle, move_direction)
			moves+=1
		else:
			print("Invalid move. Use 'W/A/S/D' to move the tiles or 'Q' to quit.")

if __name__ == "__main__":
	main()
