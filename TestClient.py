from socket import *
from ClientProtocol import Protocol

import os

from TicTacTocBoard import TicTacTocBoard

serverName = 'localhost'
serverPort = 50000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

loginLoop = True
newBoard = None
username = None
yourSymbol = None
theirSymbol = None
yourTurn = None

def printFromServer(s):
    global newBoard, username, yourSymbol, theirSymbol, yourTurn

    protocol = Protocol(s.recv(1024).decode())
    error, error_status = protocol.getError()
    singMessage = None

    if error:
        print "Error from server with status " + str(error_status)
    else:
        messages = protocol.getMessages()

        for mes in messages:
            singMessage = mes
            error, error_status = mes.getError()

            if error:
                print "Error from server with status " + str(error_status)
            else:
                verb, arguments = mes.getInfo()

                if verb == "SUCCESS":
                    print "Request successful"
                elif verb == "GAMELIST":
                    games = arguments[0]
                    print games
                elif verb == "PLAYERLIST":
                    players = arguments[0]
                    print players
                elif verb == "NEWGAME":
                    fromPlayer = arguments[0]

                    if fromPlayer == uname:
                        yourSymbol = "X"
                        theirSymbol = "O"
                        yourTurn = False
                    else:
                        yourSymbol = "O"
                        theirSymbol = "X"
                        yourTurn = True

                    newBoard = TicTacTocBoard(None, None, None)

                    print "NEW GAME FROM " + fromPlayer + " YOU ARE SYMBOL " + yourSymbol

                    if yourTurn:
                        print "MAKE A MOVE"
                    else:
                        print "WAITING ON OTHER PLAYER"

                    print(newBoard)
                elif verb == "NEWMOVE":
                    fromPlayer = arguments[0]
                    place = arguments[1]

                    if fromPlayer == uname:
                        symbol = yourSymbol
                        yourTurn = False
                    else:
                        symbol = theirSymbol
                        yourTurn = True

                    newBoard.makeMove(place, symbol)

                    if yourTurn:
                        print "MAKE A MOVE"
                    else:
                        print "WAITING ON OTHER PLAYER"

                    print(newBoard)
                elif verb == "WONGAME":
                    winner = arguments[0]

                    print winner + " WON THE GAME!!!"
                elif verb == "PLAYEREXIT":
                    fromPlayer = arguments[0]

                elif verb == "NOTTURN":
                    print "IT IS NOT YOUR TURN!!!"
                elif verb == "ILLEGALMOVE":
                    print "MOVE ISN'T LEGAL"
                elif verb == "PLAYYOURSELF":
                    print "YOU CAN'T PLAY YOURSELF"
                elif verb == "PLAYERNOTFOUND":
                    print "PLAYER NOT FOUND"

    return singMessage


def handleServerResponse(s):
    while True:
        printFromServer(s)


while(loginLoop):
    uname = raw_input('Login: Input username\n').encode()

    clientSocket.send("LOGIN " + uname.encode())
    singMes = printFromServer(clientSocket)

    error, error_status = singMes.getError()

    if error:
        print "Error from server with status " + str(error_status)
    else:
        verb, arguments = singMes.getInfo()

        if verb == "SUCCESS":
            loginLoop = False
            username = uname
        elif verb == "USERNAMETAKEN":
            print "Username is taken"


newpid = os.fork()

if newpid == 0:
    handleServerResponse(clientSocket)
else:
    while True:
        request = raw_input('Input Request:\n')
        clientSocket.send(request.encode())

# clientSocket.close()