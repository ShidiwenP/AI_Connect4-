# global variable to determine size of board
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

# displays thet board by joining all the created arrays in intiialize_board() together
def display_board(board):
    print()
    for row in board:
        print('| '.join(row))
    print()
    print()

# searches from the bottom of the board upward to find the lowest empty row in the given column
def get_next_open_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == '⚪':
            return row
    # returns None if the column is completely full
    return None

# places a piece in the lowest available row of the given column
# returns False if the column is full, True if the piece was placed successfully
def insert(board, col, piece):
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

# scores a window of 4 consecutive cells based on how many pieces each player has in it
# used by score_board() to evaluate how favorable the board is for the AI
# connect 4 heuristics taken from Keith Galli
# Resource Used: https://www.youtube.com/watch?v=MMLtza3CZFM&list=PLFCB5Dp81iNV_inzM-R9AKkZZlePCZdtV&index=6
def score_window(window, piece):
    # determine the opponent's piece based on the current piece
    if piece == '🔴':
        opponent = '🟡'
    else:
        opponent = '🔴'

    score = 0

    # heavily reward a completed window of 4
    if window.count(piece) == 4:
        score += 100

    # reward 3 in a row with an open space
    elif window.count(piece) == 3 and window.count('⚪') == 1:
        score += 5

    # reward 2 in a row with two open spaces
    elif window.count(piece) == 2 and window.count('⚪') == 2:
        score += 2

    # penalize if the opponent is about to win in this window
    if window.count(opponent) == 3 and window.count('⚪') == 1:
        score -= 4

    return score


# evaluates the entire board and returns a heuristic score from the AI's perspective
# positive scores favor the AI, negative scores favor the human
def score_board(board, ai_piece, human_piece, ai_bomb, ai_double, human_bomb, human_double):
    score = 0

    # bias toward the center column since it opens up the most winning combinations
    center_col = COLS // 2
    for r in range(ROWS):
        if board[r][center_col] == ai_piece:
            score += 3

    # score all horizontal windows of 4
    for r in range(ROWS):
        for c in range(COLS - 3):
            window = []
            for i in range(4):
                window.append(board[r][c + i])
            score += score_window(window, ai_piece)

    # score all vertical windows of 4
    for c in range(COLS):
        for r in range(ROWS - 3):
            window = []
            for i in range(4):
                window.append(board[r + i][c])
            score += score_window(window, ai_piece)

    # score all diagonal (down-right) windows of 4
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = []
            for i in range(4):
                window.append(board[r + i][c + i])
            score += score_window(window, ai_piece)

    # score all diagonal (down-left) windows of 4
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            window = []
            for i in range(4):
                window.append(board[r + i][c - i])
            score += score_window(window, ai_piece)

    # because powerups should be treated as resources, we 
    # reward the AI for still having powerups available
    if ai_bomb:
        score += 15
    if ai_double:
        score += 10

    # penalize if the human still has powerups, as this would imply the AI has
    # less resources
    if human_bomb:
        score -= 15
    if human_double:
        score -= 10

    return score

# returns a list of columns that are not yet full
def get_valid_cols(board):
    # collect every column that still has at least one open row
    valid = []
    for c in range(COLS):
        if board[0][c] == '⚪':
            valid.append(c)
    return valid


# checks if the game has reached an end state (someone won or the board is full)
def is_terminal(board, ai_piece, human_piece):
    # the game is over if either player has won or the board is completely full
    if check_winner(board, ai_piece):
        return True
    if check_winner(board, human_piece):
        return True
    if is_board_full(board):
        return True
    return False


# generates all possible moves for a player, including powerups if they still have them
# returns a list of (action, column) tuples
def generate_moves(board, has_bomb, has_double):
    valid_cols = get_valid_cols(board)
    moves = []
    # add a normal drop for every non-full column
    for col in valid_cols:
        moves.append(('drop', col))
    if has_bomb:
        # can bomb any column (even full ones — clears the whole column)
        for col in range(COLS):
            moves.append(('bomb', col))
    if has_double:
        # add a double drop for every non-full column
        for col in valid_cols:
            moves.append(('double', col))
    return moves


# applies a move to the board and returns undo info so it can be reversed later
# lets alpha_beta() simulate moves
def make_move(board, action, col, piece):
    if action == 'drop':
        row = get_next_open_row(board, col)
        board[row][col] = piece
        # save the row so unmake_move() knows which cell to clear
        return ('drop', col, row)

    elif action == 'bomb':
        # save the entire column's state before clearing it
        saved = [board[r][col] for r in range(ROWS)]
        bomb_column(board, col)
        return ('bomb', col, saved)

    elif action == 'double':
        # place two pieces stacked in the same column
        row1 = get_next_open_row(board, col)
        board[row1][col] = piece
        row2 = get_next_open_row(board, col)
        if row2 is not None:
            board[row2][col] = piece
        return ('double', col, row1, row2)


# reverses a move using the undo info returned by make_move()
# restores the board to its previous state after the AI finishes evaluating a branch
def unmake_move(board, undo_info):
    action = undo_info[0]

    if action == 'drop':
        # clear the single placed piece
        _, col, row = undo_info
        board[row][col] = '⚪'

    elif action == 'bomb':
        # restore the saved column state from before the bomb
        _, col, saved = undo_info
        for r in range(ROWS):
            board[r][col] = saved[r]

    elif action == 'double':
        # clear both placed pieces in reverse order
        _, col, row1, row2 = undo_info
        if row2 is not None:
            board[row2][col] = '⚪'
        board[row1][col] = '⚪'


# minimax algorithm with alpha-beta pruning to find the best move for the AI
# recursively explores future game states up to the given depth
# alpha = best score the maximizer can guarantee, beta = best score the minimizer can guarantee
# Resource Used: Video by Keith Galli on Connect 4 AI 
# 1. https://www.youtube.com/watch?v=MMLtza3CZFM&list=PLFCB5Dp81iNV_inzM-R9AKkZZlePCZdtV&index=6
# 2. Alpha Beta Search Pseudocode from Artificial Intelligence - A Modern Approach Textbook
def alpha_beta(board, depth, alpha, beta, maximizing, ai_piece, human_piece,
               ai_bomb, ai_double, human_bomb, human_double):
    terminal = is_terminal(board, ai_piece, human_piece)

    # base case - return a score if we've hit a terminal state or the depth limit
    if depth == 0 or terminal:
        if terminal:
            if check_winner(board, ai_piece):
                return None, 10000       # ai won
            elif check_winner(board, human_piece):
                return None, -10000      # human won
            else:
                return None, 0                # draw
        # depth limit reached, use the heuristic to evaluate the board
        return None, score_board(board, ai_piece, human_piece,
                                 ai_bomb, ai_double, human_bomb, human_double)

    # MAX-VALUE - ai's turn, wants to find the highest scoring move
    if maximizing:
        moves = generate_moves(board, ai_bomb, ai_double)
        value = float('-inf')
        best_move = moves[0]

        for action, col in moves:
            # track which powerups remain after this move
            new_ai_bomb = False if action == 'bomb' else ai_bomb
            new_ai_double = False if action == 'double' else ai_double

            undo = make_move(board, action, col, ai_piece)
            _, new_score = alpha_beta(board, depth - 1, alpha, beta, False,
                                      ai_piece, human_piece,
                                      new_ai_bomb, new_ai_double,
                                      human_bomb, human_double)
            unmake_move(board, undo)

            if new_score > value:
                value = new_score
                best_move = (action, col)

            # update alpha to be the best score the maximizer has found so far
            if value > alpha:
                alpha = value

            # beta cutoff - the minimizer already has a better option elsewhere, stop searching
            if alpha >= beta:
                break

        return best_move, value

    # MIN-VALUE - human's turn, wants to find the lowest scoring move
    else:
        moves = generate_moves(board, human_bomb, human_double)
        value = float('inf')
        best_move = moves[0]

        for action, col in moves:
            # track which powerups remain after this move
            new_human_bomb = False if action == 'bomb' else human_bomb
            new_human_double = False if action == 'double' else human_double

            undo = make_move(board, action, col, human_piece)
            _, new_score = alpha_beta(board, depth - 1, alpha, beta, True,
                                      ai_piece, human_piece,
                                      ai_bomb, ai_double,
                                      new_human_bomb, new_human_double)
            unmake_move(board, undo)

            if new_score < value:
                value = new_score
                best_move = (action, col)

            # update beta to be the best score the minimizer has found so far
            if value < beta:
                beta = value

            # alpha cutoff - the maximizer already has a better option elsewhere, stop searching
            if alpha >= beta:
                break

        return best_move, value

# function that represents the players dropping a bomb, looks at the column the player chose to bomb
# and sets every row in that column to be empty
def bomb_column(board, col):
    for row in range(ROWS):
        board[row][col] = '⚪'

# function to allow players to double drop pieces. It also checks if the board is filled before allowing
# a player to drop 2 pieces
def double_drop(board, col, piece):
    first = insert(board, col, piece)
    if not first:
        return False
    second = insert(board, col, piece)
    if not second:
        return True
    return True

# function to prompt the current player to choose an action 
# (drop, bomb, or double drop) and a column, then returns both.

# return -a tuple is then used in start_game() as action, col to determine how
# the board changed
def get_player_action(player, piece, has_bomb, has_double):
    while True:
        if not has_bomb and not has_double:
            print(f"Player {player} ({piece})")
            return 'drop', get_column_choice()
        print(f"Player {player} ({piece}), choose an action:")
        print("  1. Drop a piece")
        options = ['1']
        if has_bomb:
            print("  2. Bomb a column")
            options.append('2')
        if has_double:
            print("  3. Double drop (2 pieces in one column)")
            options.append('3')
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

    board = initialize_board()
    players = [('1', '🟡',), ('2', '🔴')]
    # sets the players abilities to true at the start of the game
    bombs = {'1': True, '2': True}
    doubles = {'1': True, '2': True}
    turn = 0

    print("     === Connect 4 ===")
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
            if not insert(board, col, piece):
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

# main game loop that initializes the board, handles turns, and checks for win/draw conditions
def start_game():
    board = initialize_board()
    players = [('1', '🟡'), ('2', '🔴')]
    # sets the players abilities to true at the start of the game
    bombs = {'1': True, '2': True}
    doubles = {'1': True, '2': True}
    turn = 0

    # assign piece colors for AI and human
    ai_piece = '🔴'
    human_piece = '🟡'

    print("     === Connect 4 ===")

    # ask the player whether they want to play against a human or the AI
    mode = input("Play vs (1) Human  or  (2) AI? Enter 1 or 2: ").strip()

    # set vs_ai flag based on the player's choice
    if mode == '2':
        vs_ai = True
    else:
        vs_ai = False

    # depth is lower than before because powerups triple the branching factor
    ai_depth = 5

    print(f"AI is playing as 🔴")

    display_board(board)

    while True:
        player, piece = players[turn % 2]

        # check if it is the AI's turn
        if vs_ai and player == '2':
            # pass powerup state so the AI can consider using bomb / double drop
            move, _ = alpha_beta(board, ai_depth, float('-inf'), float('inf'), True,
                                 ai_piece, human_piece,
                                 bombs['2'], doubles['2'],
                                 bombs['1'], doubles['1'])
            action, col = move

            # apply the AI's chosen action to the real board
            if action == 'bomb':
                bomb_column(board, col)
                bombs['2'] = False
                print(f"AI bombed column {col + 1}!")
            elif action == 'double':
                double_drop(board, col, ai_piece)
                doubles['2'] = False
                print(f"AI double-dropped in column {col + 1}!")
            else:
                insert(board, col, ai_piece)
                print(f"AI dropped in column {col + 1}!")
            display_board(board)

        # otherwise it is a human player's turn
        else:
            action, col = get_player_action(player, piece, bombs[player], doubles[player])

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
                if not insert(board, col, piece):
                    print("That column is full! Try another.")
                    continue
                display_board(board)

        # check if the last piece placed caused a win
        if check_winner(board, piece):
            if vs_ai and player == '2':
                print("AI wins!")
            else:
                print(f"Player {player} wins!")
            break

        # if the entire board is filled with no winner, it's a draw
        if is_board_full(board):
            print("It's a draw!")
            break

        turn += 1


if __name__ == '__main__':
    start_game()