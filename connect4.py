ROWS = 6
COLS = 7

def create_board():
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print()
    for row in board:
        print('| '.join(row))
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

def check_winner(board, piece):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    # Diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    # Diagonal (down-left)
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r + i][c - i] == piece for i in range(4)):
                return True
    return False

def is_board_full(board):
    return all(board[0][c] != '.' for c in range(COLS))

def get_player_move(player, piece):
    while True:
        try:
            col = int(input(f"Player {player} ({piece}), choose column (1-7): ")) - 1
            if 0 <= col < COLS:
                return col
            print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Enter a number.")

def play():
    board = create_board()
    players = [('1', 'X'), ('2', 'O')]
    turn = 0

    print("=== Connect 4 ===")
    print_board(board)

    while True:
        player, piece = players[turn % 2]
        col = get_player_move(player, piece)

        if not drop_piece(board, col, piece):
            print("That column is full! Try another.")
            continue

        print_board(board)

        if check_winner(board, piece):
            print(f"Player {player} wins!")
            break

        if is_board_full(board):
            print("It's a draw!")
            break

        turn += 1

if __name__ == '__main__':
    play()