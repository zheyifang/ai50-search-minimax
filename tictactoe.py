"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = 0
    countO = 0
    for row in board:
        for cell in row:
            if cell == X:
                countX += 1
            elif cell == O:
                countO += 1

    if countX == countO:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possMovs = set()
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                possMovs.add(( row, col ))
    
    return possMovs


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    bd = copy.deepcopy(board)
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2 or bd[action[0]][action[1]] != EMPTY:
        raise ValueError("Invalid action!")
    
    bd[action[0]][action[1]] = player(bd)

    return bd


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0] != EMPTY and row[0] == row[1] and row[1] == row[2]:
            return row[0]
        
    for i in range(3):
        if board[0][i] != EMPTY and board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]
        
    if board[1][1] != EMPTY and ((board[0][0] == board[1][1] and board[1][1] == board[2][2]) or 
                                 (board[2][0] == board[1][1] and board[0][2] == board[1][1])):
        return board[1][1]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    filled = is_filled(board)

    if filled or winner(board):
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Only be called if terminal(board) returns True
    """
    result = winner(board)

    if result == X:
        return 1
    elif result == O:
        return -1
    else:
        return 0
    

def is_filled(board):
    """
    Returns the True if all cells are filled in board, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
            
    return True


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Implemented with alpha-beta pruning
    """
    if terminal(board):
        return None
    
    maximizing = True
    if player(board) == O:
        maximizing = False

    # print("start searching...")
    move = alpha_beta(board, -2, 2, maximizing)[1]

    return move


def alpha_beta(board, alpha, beta, maximizing):
    """
    Returns the optimal action for the current player on the board
    with alpha beta pruning depending on given goal
    """
    if terminal(board):
        return (utility(board), (-1, -1))
    
    # spawn children
    children = list()
    for action in actions(board):
        children.append((result(board, action), action))

    move = None
    if maximizing:
        value = -2
        for child in children:
            # update max for curr
            curr = alpha_beta(child[0], alpha, beta, False)
            if curr[0] > value:
                value = curr[0]
                move = child[1]
            # cut off beta
            if value > beta:
                break
            alpha = max(alpha, value)
    else:
        value = 2
        for child in children:
            curr = alpha_beta(child[0], alpha, beta, True)
            if curr[0] < value:
                value = curr[0]
                move = child[1]
            if value < alpha:
                break
            beta = min(beta, value)

    # if maximizing:
    #     print(f"max move: {move} with value: {value} for board {board}")
    # else:
    #     print(f"min move: {move} with value: {value} for board {board}")

    return (value, move)
