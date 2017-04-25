from TicTacTocBoard import TicTacTocBoard
from random import random
XSYMBOL = "X"
OSYMBOL = "O"
player1 = None
player2 = None
currentPlayer= None
if (random() <= 0.5):
    player1 = XSYMBOL
    player2 = OSYMBOL
    currentPlayer = player1
else:
    player1 = OSYMBOL
    player2 = XSYMBOL
    currentPlayer = player2
newBoard = TicTacTocBoard()
while(not (newBoard.isOver()[0])):
    if (currentPlayer == player1):
        print ("1's turn")
    else:
        print("2's turn")
    print(newBoard)
    s = int(input(currentPlayer + " Input position to place marker: "))
    while (not newBoard.makeMove(s, currentPlayer)):
        #Repeat if fail.
        print(newBoard)
        s = int(input(currentPlayer +"  Input position to place marker: "))
    if (currentPlayer == player1):
        currentPlayer = player2
    else:
        currentPlayer = player1
ret,loser = newBoard.isOver()
print(newBoard)
if (loser == player1):
    print("PLAYER 2 WINS")
elif (loser == player2):
    print("PLAYER 1 WINS")
else:
    print("DRAW")
