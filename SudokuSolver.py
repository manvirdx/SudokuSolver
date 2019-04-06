import numpy as np
import time

# Load sudokus
sudokus = np.load("sudokus.npy")
print("Shape of one sudoku array:", sudokus[0].shape, ". Type of array values:", sudokus.dtype)

# Load solutions
solutions = np.load("sudoku_solutions.npy")
print("Shape of one sudoku solution array:", solutions[0].shape, ". Type of array values:", solutions.dtype, "\n")

# Print the first sudoku...
print("Sudoku #1:")
print(sudokus[0], "\n")

# ...and its solution
print("Solution of Sudoku #1:")
print(solutions[0])

#All deprecated methods are commented out

def check_possible_values(sudoku, row, col):
    #Assume all values from 1-9 are possible values
    all_possible_values = [1,2,3,4,5,6,7,8,9]
    for i in range(0,9):
        #If the cell is not equals to zero, then it checks the value in the cell and removes it from all_possible_values
        a = int(sudoku[row][i])
        if (a != 0): 
            all_possible_values[a - 1] = False
        
        b = int(sudoku[i][col])
        if (b != 0):
            all_possible_values[b - 1] = False
    
    #Definition of the starting cell in the 3x3, this applies to all of them in the sudoku
    start_row_3x3 = row - (row % 3)
    start_col_3x3 = col - (col % 3)
    
    #Same check as before but for each 3x3 box the cell corresponds to
    for i in range(0,3):
        for j in range(0,3):
            a = int(sudoku[start_row_3x3 + i][start_col_3x3 + j])
            if (a != 0):
                all_possible_values[a - 1] = False
    return all_possible_values

def depth_first_search(sudoku, row, col):
    if row == 9:
        return sudoku
    
    cells_checked_in_row = row
    cells_checked_in_col = col + 1
    if (cells_checked_in_col == 9):
        cells_checked_in_row += 1
        cells_checked_in_col = 0
    
    #If the cell is not filled with zero, then it is already done
    if (sudoku[row][col] != 0):
        return depth_first_search(sudoku, cells_checked_in_row, cells_checked_in_col)
    
    possible_values = check_possible_values(sudoku, row, col)
    for n in range(0,9):
        if possible_values[n]:
            sudoku[row][col] = 1 + n 
            #Call function recursively but with cell fitted
            sudoku_with_new_cell = depth_first_search(sudoku, cells_checked_in_row, cells_checked_in_col)
            #Checks if all iterations are valid for each new cell added
            if sudoku_with_new_cell.all():
                return sudoku_with_new_cell
    sudoku[row][col] = 0 
    return sudoku

def sudoku_solver(sudoku):
    starting_row_index = 0
    starting_col_index = 0
    
    #If not all calls of the depth first search return the sudoku plus the new cell,
    #it is invalid and the sudoku thus returns an array full of -1's as per the spec requirements
    solved_sudoku = depth_first_search(sudoku, starting_row_index, starting_col_index)
    if not solved_sudoku.all():
        solved_sudoku = np.full((9,9),float(-1))
    return solved_sudoku

total_time_taken = 0

def main():
    for i in range(len(sudokus)):
        start = time.time()
        sudoku = sudokus[i].copy()
        print("This is sudoku number", i)
        print(sudoku)
        your_solution = sudoku_solver(sudokus[i])
        print("This is your solution for sudoku number", i)
        print(your_solution)
        print("Is your solution correct?")
        print(np.array_equal(your_solution, solutions[i]))
        end = time.time()
        time_taken = (end - start)
        print(time_taken, "seconds for puzzle", i)
        total_time_taken += time_taken

print("All puzzles took {0} seconds to solve".format(total_time_taken))
