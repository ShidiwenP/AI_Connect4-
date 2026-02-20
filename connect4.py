ROWS = 6
COLS = 7

def create_board():
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print()
    for row in board:
        print('| | '.join(row))
    print()
    print()

def get_next_open_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == '.':
            return row
    return None

def drop_piece(board, col, piece):
    row = get_next_open_row(board, col)
    if row is None:
        return False
    board[row][col] = piece
    return True

if __name__ == '__main__':
    board = create_board()
    print_board(board)