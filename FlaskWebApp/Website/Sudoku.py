# Define the Sudoku board



def sudoku_solve(board):
    board1 = board
    # output_board = {}
    """
    for key, value in board.items():
        row = []
        for val in value:
            row.append(int(val))
            # print(val)

        board1.append(row)
    

    for row in range(0, 9):
        print(board1[row])
        val_f = ''
        for column in range(0, 9):
            # print(val_f)
            # print(board1[row][column])
            val_f = val_f + str(board1[row][column])
        output_board.update({'row-' + str(row)+'-solution': val_f})
    """
    # board1 = board
    solve(board1)
    return board1


# Define the solve function
def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(board, i, row, col):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False


# Define the valid function
def valid(board, num, row, column):
    # Check row
    for i in range(9):
        if board[row][i] == num and column != i:
            return False

    # Check column
    for i in range(9):
        if board[i][column] == num and row != i:
            return False

    # Check 3x3 square
    box_x = column // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != (row, column):
                return False

    return True


# Define the find_empty function
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None

# Test the solver function with sample input

