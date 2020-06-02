import turtle
import functools
import random
import math
import time

from copy import deepcopy

t = turtle.Turtle()
s = turtle.Screen()
t.hideturtle()
width = 600.0
height = 600.0
s.setup(height, width)
s.bgcolor('forest green')
gameBoard = []

def logistical(x):
    L = 1.0
    k = 5
    a = 0

    return L / (1 + math.exp(-k*(x-a)))

def drawBoard():
    t.color('black')
    t.pensize(2)
    for r in list(range(9)):
        t.penup()
        t.goto(-200, 200-(r*50))
        t.pendown()
        t.forward(400)

    t.penup()
    t.right(90)
    t.goto(-200, 200)

    for c in list(range(9)):
        t.penup()
        t.goto(-200+(c*50), 200)
        t.pendown()
        t.forward(400)

    t.penup()
    t.goto(-200, 200)
    t.left(90)

    t.pendown()
    t.pensize(7)
    for i in range(4):
        t.forward(400)
        t.right(90)
    t.penup()

def whichRow(y):
    if y > 200 or y < -200:
        return -1
    return 8 - int((y+200)/50) - 1

def whichColumn(x):
    if x > 200 or x < -200:
        return -1
    if x == 200:
        return 7
    return int((x+200)/50)

def xFromColumn(c):
    return -175 + c*50

def yFromRow(r):
    return 175 - r*50

def stampPlayer(row, column, player):
    t.color(player)
    t.goto(xFromColumn(column), yFromRow(row))
    t.pendown()
    t.shape('circle')
    t.shapesize(2, 2)
    t.stamp()
    t.penup()

def updateBoard(board, player, row, col):
    board[row][col] = player
    return board

def calculateScore(board, player):
    sum = 0
    for r in board:
        sum += len([v for v in r if v == player])
    return sum

def updateScore():
    global gameBoard
    whiteScore = calculateScore(gameBoard, 'white')
    blackScore = calculateScore(gameBoard, 'black')

    textSize = 30

    t.goto(-200, 250 - textSize/2 - textSize/4)
    t.pendown()
    t.pencolor('black')
    t.write(str(whiteScore), align = 'center', font = ('Avenir',textSize, 'bold'))
    t.penup()

    t.goto(200, 250 - textSize/2 - textSize/4)
    t.pendown()
    t.pencolor('white')
    t.write(str(blackScore), align = 'center', font = ('Avenir',textSize, 'bold'))
    t.penup()

    return (whiteScore, blackScore)

def drawScore():
    t.color('white')
    t.goto(-200, 250)
    t.pendown()
    t.shape('circle')
    t.shapesize(3.5, 3.5)
    t.stamp()
    t.penup()

    t.color('black')
    t.goto(200, 250)
    t.pendown()
    t.shape('circle')
    t.shapesize(3.5, 3.5)
    t.stamp()
    t.penup()
    t.hideturtle()

def initialize():
    global gameBoard
    global player
    global turnCount

    t.clear()
    gameBoard = [[0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]]
    player = 'white'
    turn = 1

    gameBoard[3][3] = 'white'
    gameBoard[3][4] = 'black'
    gameBoard[4][3] = 'black'
    gameBoard[4][4] = 'white'
    s.tracer(0, 0)
    update()

def allMoves(board, player):
    l = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == 0 and validMove(board, player, r, c):
                l.append([r, c])
    return l

def validMove(board, player, row, column):

    def checkDirection(r, c, vec, player): #vec = [+row, +col] vector
        if r+vec[0] < 0 or r+vec[0] > 7 or c+vec[1] > 7 or c+vec[1] < 0:
            return False

        if board[r+vec[0]][c+vec[1]] == player:
            return board[r][c] != player and board[r][c] != 0

        elif board[r+vec[0]][c+vec[1]] == 0:
            return False

        else:
            return checkDirection(r+vec[0], c+vec[1], vec, player)

    if board[row][column] != 0:
        return False

    vectors = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]

    for v in vectors:
        if checkDirection(row, column, v, player):
            return True
    return False

def nextBoard(board, player, move):

    def moveDirection(r, c, vec, player, path=[]):
        if r+vec[0] < 0 or r+vec[0] > 7 or c+vec[1] > 7 or c+vec[1] < 0:
            return []

        if board[r+vec[0]][c+vec[1]] == player:
            if board[r][c] != player and board[r][c] != 0:
                return path + [[r, c]]
            return []

        elif board[r+vec[0]][c+vec[1]] == 0:
            return []

        else:
            return moveDirection(r+vec[0], c+vec[1], vec, player, path+[[r, c]])

    vectors = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
    overall = [x for x in [moveDirection(move[0], move[1], v, player) for v in vectors] if x != []]

    if overall != []:
        updates = flatten(overall) + [[move[0], move[1]]]
    else:
        updates = []

    bCopy = deepcopy(board)
    for u in updates:
        bCopy[u[0]][u[1]] = player

    return bCopy

def updateBoardDisplay():
    global gameBoard

    for r in list(range(8)):
        for c in list(range(8)):
            if gameBoard[r][c] != 0:
                stampPlayer(r, c, gameBoard[r][c])

def showMoves(moves):
    global player
    l = []
    for m in moves:
        t.goto(xFromColumn(m[1]),yFromRow(m[0]))
        t.color(player)
        t.pendown()
        t.shape('circle')
        t.shapesize(0.5, 0.5)
        t.stamp()
        t.penup()

def playerMove(r, c):
    global gameBoard
    global player

    if validMove(gameBoard, player, r, c):
        return [r, c]
    else:
        print("Invalid Move")
        return []

def takeTurn(x, y):
    global player

    if x > 200 or x < -200 or y > 200 or y < -200:
        initialize()
    else:
        if allMoves(gameBoard, player) == []:
            print(player+" can't move!")
            p1 = False
        else:
            p1 = playerMove(whichRow(y), whichColumn(x))
        if p1 == []:
            return
        elif p1 != False:
            makeMove(p1[0], p1[1], player)

        update()

        p2 = compMoveW()
        if p2 == []:
            print("AI can't move.")
            return
        elif p2 != False:
            makeMove(p2[0], p2[1], player)

        update()

def AIMove():
    global gameBoard
    global player

    if player == 'white':
        move = compMoveW()
    elif player == 'black':
        move = compMoveB()
    if move != False:
        makeMove(move[0], move[1], player)
        update()

def makeMove(r, c, player):
    global gameBoard
    gameBoard = nextBoard(gameBoard, player, [r, c])

def evaluation(board, player, turnCount):

    opp = swapPlayer(player)

    def getEdgeSum(p):
        edgeSum = 0
        for i in range(8):

            edgeSum += board[0][i] == p
            edgeSum += board[i][0] == p
            edgeSum += board[7][i] == p
            edgeSum += board[i][7] == p

        return edgeSum

    def getCornerSum(p):
        cornerSum = 0
        cornerSum += board[0][0] == p
        cornerSum += board[7][7] == p
        cornerSum += board[0][7] == p
        cornerSum += board[7][0] == p

        return cornerSum

    score = (calculateScore(board, player))/64
    scoreW = (turnCount/64 - 0.5)

    if turnCount >= 50:
        return score*scoreW

    edgeAdvantage = (getEdgeSum(player) - getEdgeSum(opp))/28
    edgesW = 0.1

    moveAdvantage = (len(allMoves(gameBoard, player)) - len(allMoves(gameBoard, opp)))/10
    moveW = 0.75

    cornerAdvantage = (getCornerSum(player) - getCornerSum(opp))/4
    cornerW = 0.99

    sum = score*scoreW + cornerAdvantage*cornerW + moveAdvantage*moveW + edgeAdvantage*edgesW

    return logistical(sum)

def combinedSearchBA(board, player, depth):

    opp = swapPlayer(player)
    turnCount = calculateScore(board, player) + calculateScore(board, opp)

    if turnCount < 10:
        depth = 5
    elif turnCount < 30:
        depth = 5
    elif turnCount < 45:
        depth = 4
    elif turnCount < 50:
        depth = 6
    elif turnCount < 60:
        depth = 8
    else:
        depth = 11

    depth -= 1

    def minOpp(move, depth, board, alpha, beta):
        if move != []:
            nBoard = nextBoard(board, player, move)
        else:
            nBoard = board

        pMoves = allMoves(nBoard, opp)

        if depth == 0:
            return evaluation(nBoard, player, turnCount)

        if pMoves == []:
            pMoves.append([])

        v = 100

        for m in pMoves:
            v = min([v, maxPlayer(m, depth-1, nBoard, alpha, beta)])
            if v <= alpha:
                return v
            beta = min([beta, v])
        return v

    def maxPlayer(move, depth, board, alpha, beta):
        if move != []:
            nBoard = nextBoard(board, opp, move)
        else:
            nBoard = board

        pMoves = allMoves(nBoard, player)

        if depth == 0:
            return evaluation(nBoard, player, turnCount)

        if pMoves == []:
            pMoves.append([])

        v = -100

        for m in pMoves:
            v = max([v, minOpp(m, depth-1, nBoard, alpha, beta)])
            if v >= beta:
                return v
            alpha = max([alpha, v])

        return v

    def movePreScore(m):
        return minOpp(m, 1, board, -100, 100)

    moves = allMoves(board, player)

    if len(moves) == 1:
        return moves[0]

    start = time.time()

    moves.sort(key=movePreScore, reverse=True)

    choices = [minOpp(m, depth-1, board, -100, 100) for m in moves]

    return moves[choices.index(max(choices))]

def compMoveW():
    global gameBoard
    global player

    pMoves = allMoves(gameBoard, player)
    depth = 5

    if pMoves != []:
        s = time.time()
        m = combinedSearchBA(gameBoard, player, depth)
        print(player, time.time()-s)
        return m

    else:
        print("AI Can't move")
        return False

def compMoveB():
    global gameBoard
    global player

    depth = 5
    pMoves = allMoves(gameBoard, player)

    if pMoves != []:
        s = time.time()
        move = minimax(gameBoard, player, depth, float('inf'), -float('inf'))
        print(player, time.time()-s)
        return move
    else:
        print("AI Can't move")
        return False

def compMove():
    global gameBoard
    global player

    pMoves = allMoves(gameBoard, player)

    if pMoves != []:
        return random.choice(allMoves(gameBoard, player))
    else:
        print("AI Can't move")
        return False

def swapPlayer(player):
    if player == 'white':
        return 'black'
    else:
        return 'white'

def main():
    global gameBoard
    global player
    turtle.onscreenclick(takeTurn)

    if not 0 in flatten(gameBoard):
        print(flatten(gameBoard))
        gameOver()
    else:
        pass

    # while 0 in flatten(gameBoard) and len(allMoves(gameBoard, 'white')) + len(allMoves(gameBoard, 'black')) != 0:
    #     AIMove()

def flatten(l):
    r = []
    for sl in l:
        r+=sl
    return r

def gameOver():
    global evaluations

    scores = updateScore()
    wScore = scores[0]
    bScore = scores[1]

    if wScore > bScore:
        print('White Wins')
    else:
        print("Black Wins")

def updateMoves():
    global player
    global gameBoard

    pMoves = allMoves(gameBoard, player)
    if pMoves == []:
        player = swapPlayer(player)

    showMoves(pMoves)

def writeOthello():
    #Othello Text
    t.goto(0, 225)
    t.pencolor('black')
    t.write('Othello', align = 'center', font = ('Avenir',50, 'bold', 'underline'))
    t.goto(2, 220)
    t.pencolor('white')
    t.write('Othello', align = 'center', font = ('Avenir',50, 'bold', 'underline'))
    s.tracer(0, 1)

def update():
    global player
    global gameBoard

    player = swapPlayer(player)
    t.clear()

    writeOthello()
    drawBoard()
    updateBoardDisplay()
    drawScore()
    updateScore()
    updateMoves()

initialize()
main()
