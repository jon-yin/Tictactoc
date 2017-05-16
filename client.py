import sys
from socket import *
from ClientProtocol import Protocol

import os
from TicTacTocBoard import TicTacTocBoard

#Extract host and port from arguments
argv = sys.argv
host = argv[1]
port = int(argv[2])

#Connect to server.
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((host, port))

#Checks if need to login
loginLoop = True
newBoard = None
username = None
yourSymbol = None
theirSymbol = None
yourTurn = None

# The main way the client will handle reponse from the server, this is done by an entirely seperate process.
def printFromServer(s):
    global newBoard, username, yourSymbol, theirSymbol, yourTurn
    decodedString = s.recv(1024).decode()
    #Use client protocol to do error checking on server message.
    protocol = Protocol(decodedString)
    error, error_status = protocol.getError()
    singMessage = None

    #If the client protocol detects an error, then print out the error and don't parse the message.
    if error:
        print "Error from server with status " + str(error_status)
    else:
        #Check all pending messages that the client has recieved from the server.
        messages = protocol.getMessages()

        for mes in messages:
            singMessage = mes
            error, error_status = mes.getError()

            if error:
                print "Error from server with status " + str(error_status)
            else:
                verb, arguments = mes.getInfo()
                #If client protocol determines that this was from a successful request
                if verb == "SUCCESS":
                    print "Request successful"
                #Check if client requested for the list of all games.
                elif verb == "GAMELIST":
                    #games are in the arguments supplied by the server.
                    games = arguments[0]

                    #Prints a list of all games.
                    print "List of Games"
                    print "---------------"

                    #Format and print every game.
                    for gm in games:
                        print str(str(gm[0]) + ": " + gm[1] + " VS. " + gm[2])
                #Check if client requested the list of all players.
                elif verb == "PLAYERLIST":
                    #Player usernames and their statuses are supplied by the server.
                    players = arguments[0]

                    print "List of Players"
                    print "---------------"
                    #Simply prints all of the players + their status
                    for pl in players:
                        if pl[1] == 1:
                            status = "Available"
                        else:
                            status = "Busy"

                        print pl[0] + ": " + status
                #Check if client is participating in a new game.
                elif verb == "NEWGAME":
                    #The player who initiates gets symbol X. The player who initiates is supplied as a message from the server.
                    fromPlayer = arguments[0]

                    #Check whether if its this player or the opposing player that started the game.
                    if fromPlayer == uname:
                        yourSymbol = "X"
                        theirSymbol = "O"
                        yourTurn = False
                    else:
                        yourSymbol = "O"
                        theirSymbol = "X"
                        yourTurn = True
                    #The board serves to allow each client to be able to print out their own board.
                    newBoard = TicTacTocBoard(None, None, None)

                    print "NEW GAME FROM " + fromPlayer + " YOU ARE SYMBOL " + yourSymbol

                    if yourTurn:
                        print "MAKE A MOVE"
                    else:
                        print "WAITING ON OTHER PLAYER"

                    print(newBoard)
                #Client checks if a player made a move.
                elif verb == "NEWMOVE":
                    fromPlayer = arguments[0]
                    place = arguments[1]
                    #Checks to see which player made the move.
                    if fromPlayer == uname:
                        symbol = yourSymbol
                        yourTurn = False
                    else:
                        symbol = theirSymbol
                        yourTurn = True
                    #Makes the move on their individual board and prints it.
                    newBoard.makeMove(place, symbol)

                    if yourTurn:
                        print "MAKE A MOVE"
                    else:
                        print "WAITING ON OTHER PLAYER"

                    print(newBoard)
                #Checks to see if this client should print a board that the client is observing
                elif verb == "SENDBRD":
                    parts = arguments[0].split(";")
                    blankBoard = TicTacTocBoard(None,None,None)
                    #String which represents the current state of the board
                    board = parts[0]
                    blankBoard.setBoard(board)
                    #Finds player1's name and their symbol.
                    player1 = parts[1].split(":")[0]
                    symbol1 = parts[1].split(":")[1]
                    #Finds player2's name and their symbol.
                    player2 = parts[2].split(":")[0]
                    symbol2 = parts[2].split(":")[1]
                    #Find whose turn is it.
                    playerTurn = eval(parts[3])
                    #Print the board as well as the name of the match
                    print ("OBSERVING PLAYER 1: " + player1 + "(" + symbol1 + ") " + "VS: " + "PLAYER 2: " + player2 + "(" + symbol2 + ")")
                    print blankBoard
                    #Print the name of the currentPlayer's turn.
                    if (playerTurn):
                        print "It's currently " + player1 +"'s turn."
                    else:
                        print "It's currently " + player2 +"'s turn."
                #Error, the client referred to a non-existent game.
                elif verb == "GAMEDOESNTEXIST":
                    gid = arguments[0]
                    print "GAME " + gid + " DOESN'T EXIST"
                #Print who won the game if client is observer or player.
                elif verb == "WONGAME":
                    winner = arguments[0]
                    print winner + " WON THE GAME!!!"
                #Print a draw if client is observer or player.
                elif verb == "GAMEDRAW":
                    print "GAME IS A DRAW!!!"
                #Print if the other player exited in a game.
                elif verb == "PLAYEREXIT":
                    print "OTHER PLAYER HAS LEFT THE GAME!!!"
                #Error, client attempts to act not on his turn.
                elif verb == "NOTTURN":
                    print "IT IS NOT YOUR TURN!!!"
                #Error, client makes an invalid move.
                elif verb == "ILLEGALMOVE":
                    print "MOVE ISN'T LEGAL"
                #Error, client attempts to initiate a game with itself.
                elif verb == "PLAYYOURSELF":
                    print "YOU CAN'T PLAY YOURSELF"
                #Error, client attempts to play a non-existent player.
                elif verb == "PLAYERNOTFOUND":
                    print "PLAYER NOT FOUND"
                #Client is exiting.
                elif verb == "SAFEEXIT":
                    print "SAFE TO LEAVE, EXITING"
                    os._exit(1)
                #Print help string that server provides
                elif verb == "HELPSTR":
                    print arguments[0]
                #Error, client attempts to observe a game when busy.
                elif verb == "BUSY":
                    print "YOU'RE ALREADY CURRENTLY/OBSERVING IN A GAME\n FINISH WHAT YOU'RE DOING FIRST."
                #Print if one of the players in a game you observe has exited.
                elif verb == "OBSEXIT":
                    exiter = arguments[0]
                    print exiter + " " + "LEFT THE GAME!!!"
                #Error, client attempts to unobserve when already not observing.
                elif verb == "NOOBSERVE":
                    print "YOU ARE NOT OBSERVING A GAME"
                #Error, client attempts to unobserve a game it is not observing.
                elif verb == "WRNGGAME":
                    wrongGame = arguments[0].split(":")[0]
                    rightGame = arguments[0].split(":")[1]
                    print "YOU ARE OBSERVING GAME " + rightGame + " NOT GAME " + wrongGame
                #Client successfuly unobserves game.
                elif verb == "UNOBSERVED":
                    print "YOU SUCCESSFULLY UNOBSERVED THE GAME"
                #Error, client attempts to comment when not in a game.
                elif verb == "FREE":
                    print "CAN'T COMMENT, YOU'RE NOT IN A GAME."
                #Error, client attempts to make a move when observing
                elif verb == "CANTPLACEOBS":
                    print "CAN'T PLACE, YOU'RE ONLY OBSERVING."
                #Some player/observer has made a comment in the game that the client is currently is also in.
                elif verb == "COMMENT":
                    retStr = arguments[0]
                    retStr = retStr.replace("NEWLINE", "\n")
                    print retStr

    return singMessage

# Solely print out appopriate responses based on server response.
def handleServerResponse(s):
    while True:
        printFromServer(s)
        print("Input Request:")

#While you are not logged in.
while(loginLoop):
    #Enter a username
    uname = raw_input('Login: Input username\n').encode()

    clientSocket.send("LOGIN " + uname.encode())
    singMes = printFromServer(clientSocket)

    error, error_status = singMes.getError()
    #If error, then need to enter a new username
    if error:
        print "Error from server with status " + str(error_status)
    else:
        verb, arguments = singMes.getInfo()
        #Otherwise, allow the client to start making requests.
        if verb == "SUCCESS":
            loginLoop = False
            username = uname
            print ("Input Request:")
        elif verb == "USERNAMETAKEN":
            print "Username is taken"

#Create two different processes.
newpid = os.fork()

#Child will print responses from server.
if newpid == 0:
    handleServerResponse(clientSocket)
else:
#Parent will send messages from client to server.
    while True:
        request = raw_input('\n')
        if (request == ""):
            clientSocket.send("BLANK".encode())
        else:
            clientSocket.send(request.encode())
        if request == 'EXIT':
            clientSocket.close()
            os._exit(1)
