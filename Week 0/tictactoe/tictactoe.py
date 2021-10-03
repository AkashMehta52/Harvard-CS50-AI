"""
Tic Tac Toe Player
"""

import math

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

    #simple nested for loop to traverse array and count
    #the number of X's and O's
    for xcount in range(3):
        for yCount in range(3):
            if(board[xcount][yCount] == X):
                countX+=1
            elif(board[xcount][yCount] == O):
                countO+=1
    
    if(countX > countO):
        return O
    else: return X


def actions(board):
    """
        Returns set of all possible actions (i, j) available on the board.
    """
    #create empty action set
    actionSet = set()

    #loop over board, for all empty spaces, add coordinates to actionSet
    for x in range(3):
        for y in range(3):
            if(board[x][y] == EMPTY):
                actionSet.add((x,y))
    
    return actionSet


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #first ensure valid action
    if(action not in actions(board)):
        raise Exception("action not valid!")

    #Copy the original board
    copyBoard = [row[:] for row in board]
    i = action[0]
    j = action[1]

    #alter the copied board and return it
    copyBoard[i][j] = player(board)
    return copyBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if (board[i][0] == X):
            #check a row
            countX = 0
            for j in range(3):
                if(board[i][j] == X):
                    countX+=1
                else: break
            if(countX == 3):
                return X
            #check a column
            countX = 0
            for j in range(3):
                if(board[j][i] == X):
                    countX+=1
                else: break
            if(countX == 3):
                return X
        elif(board[i][0] == O):
            #check a row
            countO = 0
            for j in range(3):
                if(board[i][j] == O):
                    countO+=1
                else: break
            if(countO == 3):
                return O
            #check a column
            countO = 0
            for j in range(3):
                if(board[j][i] == O):
                    countO+=1
                else: break
            if(countO == 3):
                return O

    #check diagonals
    if(board[0][0] == X and board[0][0] == board[1][1] == board[2][2]):
        return X
    elif(board[0][0] == O and board[0][0] == board[1][1] == board[2][2]):
        return O
    elif(board[0][2] == X and board[0][2] == board[1][1] == board[2][0]):
        return X
    elif(board[0][2] == O and board[0][2] == board[1][1] == board[2][0]):
        return O
    else: return None


def fullBoard(board):
    """
    return true if game board is full, false otherwise.
    """
    countCells = 0
    for x in range(3):
        for y in range(3):
            if (board[x][y] != EMPTY):
                countCells += 1
    
    if(countCells == 9):
        return True
    else: return False


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if(winner(board) == X):
        return True
    elif(winner(board) == O):
        return True
    elif(fullBoard(board)):
        return True
    else: return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if(terminal(board)):
        if (winner(board) == X):
            return 1
        elif (winner(board) == O):
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #with Alpha-Beta optimization :)
    if(terminal(board)):
        return None
    #Set Max and Min for bookkeeping
    maxV = float("-inf")
    minV = float("inf")
    if(player(board) == X):
        #X is max player
        move = maxVal(board, maxV, minV)[1]
        return move

    elif(player(board) == O):
        #O is min player
        move = minVal(board, maxV, minV)[1]
        return move


def maxVal(board, maxV, minV):
    nextMove = None
    if terminal(board):
        return utility(board), None

    v = float('-inf')

    for action in actions(board):
        nextV = minVal(result(board,action), maxV, minV)[0]
        if(nextV > v):
            v = nextV
            nextMove = action
            #alpha selection
            maxV = max(maxV, v)
        #tree pruning condition
        if(maxV >= minV):
            break       
    return v, nextMove



def minVal(board, maxV, minV):
    nextMove = None
    if terminal(board):
        return utility(board), None

    v = float('inf')
  
    for action in actions(board):
        nextV = maxVal(result(board,action), maxV, minV)[0]
        if(nextV < v):
            v = nextV
            nextMove = action
            #beta selection
            minV = min(minV, v)
        #tree pruning condition
        if(maxV >= minV):
            break    
    return v, nextMove



