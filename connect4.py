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

if __name__ == '__main__':
    board = create_board()
    print_board(board)