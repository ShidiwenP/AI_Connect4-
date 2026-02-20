# global variable to allow for dimensions of board, currently it is the default 6 x 7
ROWS = 6
COLS = 7

# creates a 6 x 7 board
# uses a white circle to represent an empty space, 
# and red and yellow circles for p1 and p2 piece respectively
def initialize_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append('⚪')
        board.append(row)
    return board

# displays thet board by join all the created arrays in intiialize_board() together
def display_board(board):
    print()
    for row in board:
        print('| '.join(row))
    print()
    print()

def get_next_open_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == '⚪':
            return row
    return None

def drop_piece(board, col, piece):
    row = get_next_open_row(board, col)
    if row is None:
        return False
    board[row][col] = piece
    return True

# function to check the four win conditions - horizontal, vertical, and two diagonals
def check_winner(board, piece):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == piece
                    and board[r][c + 1] == piece
                    and board[r][c + 2] == piece
                    and board[r][c + 3] == piece):
                return True
    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if (board[r][c] == piece
                    and board[r + 1][c] == piece
                    and board[r + 2][c] == piece
                    and board[r + 3][c] == piece):
                return True
    # Diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == piece
                    and board[r + 1][c + 1] == piece
                    and board[r + 2][c + 2] == piece
                    and board[r + 3][c + 3] == piece):
                return True
    # Diagonal (down-left)
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if (board[r][c] == piece
                    and board[r + 1][c - 1] == piece
                    and board[r + 2][c - 2] == piece
                    and board[r + 3][c - 3] == piece):
                return True
    return False

# function to check if every column on the board is full, meaning the players have tied
# ⚪ is used to represent an empty space, so if all the positions are not empty, then that means
# the board is full
def is_board_full(board):
    return all(board[0][c] != '⚪' for c in range(COLS))

# function that represents the players dropping a bomb, looks at the column the player chose to bomb
# and sets every row in that column to be empty
def bomb_column(board, col):
    for row in range(ROWS):
        board[row][col] = '⚪'

# function to allow players to double drop pieces. It also checks if the board is filled before allowing
# a player to drop 2 pieces
def double_drop(board, col, piece):
    first = drop_piece(board, col, piece)
    if not first:
        return False
    second = drop_piece(board, col, piece)
    if not second:
        return True
    return True

# function to prompt the current player to choose an action 
# (drop, bomb, or double drop) and a column, then returns both.

# return -a tuple is then used in play() as action, col to determine how
# the board changed
def get_player_action(player, piece, has_bomb, has_double):
    while True:
        print(f"Player {player} ({piece}), choose an action:")
        print("  1. Drop a piece")
        options = ['1']
        if has_bomb:
            print("  2. Bomb a column")
            options.append('2')
        if has_double:
            print("  3. Double drop (2 pieces in one column)")
            options.append('3')
        if len(options) == 1:
            return 'drop', get_column_choice()
        choice = input(f"Enter {'/'.join(options)}: ").strip()
        if choice == '1':
            return 'drop', get_column_choice()
        elif choice == '2' and has_bomb:
            return 'bomb', get_column_choice()
        elif choice == '3' and has_double:
            return 'double', get_column_choice()
        else:
            print(f"Invalid choice. Enter {'/'.join(options)}.")

# function to get the column choice of the user whether for the default drop or their abilities
def get_column_choice():
    while True:
        try:
            col = int(input("Choose column (1-7): ")) - 1
            # checks if the user inputted a column that is within the global COLs boundaries
            if 0 <= col < COLS:
                return col
            print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Enter a number.")

def play():
    board = initialize_board()
    players = [('1', '🟡',), ('2', '🔴')]
    # sets the players abilities to true at the start of the game
    bombs = {'1': True, '2': True}
    doubles = {'1': True, '2': True}
    turn = 0

    print("=== Connect 4 ===")
    display_board(board)

    while True:
        # each time 'turn' increments, the game switches to the other player
        # by using the modulus remainder
        # players = [('1', 'X'), ('2', 'O')], so turn 0 would be 0 % 2 = 0, so index 0 (player 1)
        # and turn 1 would be 1 % 2 = 1, so index 1 (player 2)
        player, piece = players[turn % 2]
        action, col = get_player_action(player, piece, bombs[player], doubles[player])

        # the three actions a player can take - bomb, double drop, and regular drop
        if action == 'bomb':
            bomb_column(board, col)
            bombs[player] = False
            print(f"Player {player} bombed column {col + 1}!")
            display_board(board)
        elif action == 'double':
            if not double_drop(board, col, piece):
                print("That column is full! Try another.")
                continue
            doubles[player] = False
            print(f"Player {player} double-dropped in column {col + 1}!")
            display_board(board)
        elif action == 'drop':
            if not drop_piece(board, col, piece):
                print("That column is full! Try another.")
                continue
            display_board(board)

        # check if after the player placed a piece if they satisfied any of the win conditions
        if check_winner(board, piece):
            print(f"Player {player} wins!")
            break
        
        # if entire board is filled, announce such and break
        if is_board_full(board):
            print("It's a draw!")
            break

        turn += 1

if __name__ == '__main__':
    play()