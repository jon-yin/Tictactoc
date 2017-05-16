import select
import socket

from GameServer import GameServer
from ServerProtocol import Protocol

host = 'localhost'
port = 50000
backlog = 5
maxsize = 1024

# Start listening on our socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen(backlog)
input = [server, ]  # List of all connections we want to check for data

running = 1

# New game server instance which will help manage ongoing games
gameServer = GameServer()
# Map of socket connections to players
socketsToPlayers = {}


# Helper function to send status codes with messages to a socket
def sendStatus(soc, code, message=None):
    codeStr = "STATUS " + str(code)

    if message is not None:
        # print("The message is" + message)
        codeStr += "\n" + str(message)

    codeStr += "\r\n\r\n"

    soc.send(codeStr.encode())


# Helper function to print a board
def translateBoard(board):
    retStr = ""
    for i in board.getBoard():
        for j in i:
            if (j == None):
                retStr += str(0)
            elif (j == "X"):
                retStr += str(1)
            else:
                retStr += str(2)
    return retStr


# Helper function to print a board
def createBoardState(board):
    # Translate game state into a string.
    player1, player2 = board.getPlayers()
    retStr = translateBoard(board) + ";"
    retStr += player1.getUsername() + ":" + player1.getSymbol() + ";"
    retStr += player2.getUsername() + ":" + player2.getSymbol() + ";"
    retStr += str(board.isTurn(player1.getSymbol))
    return retStr


# Helper function to return the help command string
def resHelp():
    return "LIST OF AVAILABLE COMMANDS{n}" \
           "----------------------------------{n}" \
           "help:  Prints all available commands. SYNTAX: $HELP{n}" \
           "login: Login to the server, allowing you to both play and communicate with other players. SYNTAX: $LOGIN username{n}" \
           "who:   Get a list of all online players. SYNTAX: $WHO{n}" \
           "games: Get a list of all currently played games. SYNTAX: $GAMES{n}" \
           "play:  Start a new game with a player. SYNTAX: $PLAY username{n}" \
           "place: Make a move and place a symbol onto the board, accepts a value from 1-9. SYNTAX: $PLACE 4{n}" \
           "exit:  Quit from the current game if any and exit from the server SYNTAX: $EXIT{n}" \
           "observe:    Observes the game with the given i.d. number of the game. SYNTAX: $OBSERVE 1{n}" \
           "unobserve:  Unobserves the game with the given i.d. number of the game. You must be observing this game to start with. SYNTAX: $UNOBSERVE 1{n}" \
           "comment:    Makes a comment to the other players/observers in the current game you are playing/watching. SYNTAX: $COMMENT Hello World{n}{n}"


# Helper function to close a connection socket
def exitCommand(socket):
    socket.send("Exiting from server\n")
    socket.close()


# Helper function to determine if a socket is associated to a player
def loggedIn(ss):
    return ss in socketsToPlayers


# Helper function to return the player that is linked to a socket
def currPlayer(s):
    return socketsToPlayers[s]


while running:
    inputready, outputready, exceptready = select.select(input, [], [])

    for s in inputready:  # check each socket that select() said has available data

        if s == server:  # if select returns our server socket, there is a new
            # remote socket trying to connect
            client, address = server.accept()
            input.append(client)  # add it to the socket list so we can check it now
            print('new client added%s' % str(address))

        else:
            # select has indicated that these sockets have data available to recv
            data = s.recv(maxsize).decode()

            if data:
                # Create a new protocol instance with our data
                protocol = Protocol(data)
                error, error_status = protocol.getError()

                if error:  # The protocol was ill-formatted
                    sendStatus(s, error_status)
                else:
                    for message in protocol.getMessages():
                        error, error_status = message.getError()

                        if error:  # The message within the protocol was ill-formatted
                            sendStatus(s, error_status)
                        else:
                            verb, arguments = message.getInfo()  # Extract the info from the message

                            # Handle all possible verbs (actions)
                            # Each verb has its own logic

                            if verb == "LOGIN":
                                status, player = gameServer.login(arguments[0], s)

                                if status:
                                    sendStatus(s, 200)
                                    socketsToPlayers[s] = player
                                else:  # Username is taken
                                    sendStatus(s, 422)
                            elif verb == "GAMES":
                                if not loggedIn(s):
                                    sendStatus(s, 401)
                                else:
                                    games = gameServer.getGames()
                                    pToG = []

                                    for g in games:
                                        pToG.append(str(g[0]) + ":" + g[1] + ":" + g[2])

                                    sendStatus(s, 250, ",".join(pToG))
                            elif verb == "WHO":
                                if not loggedIn(s):
                                    sendStatus(s, 401)
                                else:
                                    players = gameServer.getPlayers()
                                    pToG = []

                                    for p in players:
                                        pToG.append(str(p[0]) + ":" + str(p[1]))

                                    sendStatus(s, 251, ",".join(pToG))
                            elif verb == "PLAY":
                                if not loggedIn(s):
                                    sendStatus(s, 401)
                                else:
                                    cPlayer = currPlayer(s)
                                    toPlayer = gameServer.getPlayer(arguments[0])

                                    if toPlayer is None:  # To player doesn't exist
                                        sendStatus(s, 404)
                                    elif cPlayer == toPlayer:  # To player is current player
                                        sendStatus(s, 409)
                                    else:
                                        status = gameServer.startNewGame(cPlayer, toPlayer)

                                        if status:
                                            # Notify both players that a new game is starting
                                            sendStatus(s, 200)
                                            sendStatus(cPlayer.getSocket(), 210, cPlayer.getUsername())
                                            sendStatus(toPlayer.getSocket(), 210, cPlayer.getUsername())
                                        else:
                                            sendStatus(s, 423)
                            elif verb == "PLACE":
                                if not loggedIn(s):
                                    sendStatus(s, 401)
                                else:
                                    cPlayer = currPlayer(s)
                                    game = cPlayer.getGame()

                                    if game is None:  # Current player isn't in a game
                                        sendStatus(s, 400)
                                    else:
                                        players = game.getPlayers()

                                        if cPlayer not in players:  # Observer can't make moves
                                            sendStatus(s, 414)
                                        elif game.isTurn(cPlayer.getSymbol()):
                                            if game.makeMove(arguments[0], cPlayer.getSymbol()):

                                                sendStatus(s, 200)

                                                # Notify everyone of the new move
                                                rstr = cPlayer.getUsername() + ":" + str(arguments[0])
                                                sendStatus(players[0].getSocket(), 201, rstr)
                                                sendStatus(players[1].getSocket(), 201, rstr)

                                                observers = game.getObservers()

                                                for i in observers:
                                                    string = createBoardState(game)
                                                    sendStatus(i.getSocket(), 220, string)

                                                # Game has been won
                                                if game.isOver()[0]:
                                                    ret, loser = game.isOver()

                                                    # Notify everyone that the game has ended with the winner
                                                    if loser == players[1].getSymbol():
                                                        sendStatus(players[0].getSocket(), 202,
                                                                   players[1].getUsername())
                                                        sendStatus(players[1].getSocket(), 202,
                                                                   players[1].getUsername())
                                                        for i in observers:
                                                            sendStatus(i.getSocket(), 202,
                                                                       players[1].getUsername())
                                                    elif loser == players[0].getSymbol():
                                                        sendStatus(players[0].getSocket(), 202,
                                                                   players[0].getUsername())
                                                        sendStatus(players[1].getSocket(), 202,
                                                                   players[0].getUsername())
                                                        for i in observers:
                                                            sendStatus(i.getSocket(), 202,
                                                                       players[0].getUsername())
                                                    else:
                                                        sendStatus(players[0].getSocket(), 203)
                                                        sendStatus(players[1].getSocket(), 203)

                                                        for i in observers:
                                                            sendStatus(i.getSocket(), 203)

                                                    gameServer.endGame(game)
                                            else:  # Illegal move
                                                sendStatus(s, 411)
                                        else:  # It isn't our turn
                                            sendStatus(s, 406)
                            elif verb == "OBSERVE":
                                if not loggedIn(s):
                                    sendStatus(s, 401)
                                else:
                                    gid = int(arguments[0])
                                    ids = []
                                    cPlayer = currPlayer(s)

                                    # Currently in a game, don't allow observation
                                    if cPlayer.status == 2 or cPlayer.status == 0:
                                        sendStatus(s, 408)

                                    for id in gameServer.getGames():
                                        ids.append(id[0])

                                    if gid in ids:
                                        # Begin to observe game.
                                        cPlayer.observeGame(gameServer.getGame(gid))

                                        # Send the board as an object back to the observer
                                        string = createBoardState(gameServer.getGame(gid))
                                        sendStatus(s, 220, string)
                                    else:
                                        # Failed to find game
                                        sendStatus(s, 410, gid)
                            elif verb == "EXIT":
                                if not loggedIn(s):
                                    sendStatus(s, 401)
                                else:
                                    game = currPlayer(s).getGame()

                                    if game is not None:
                                        gameServer.endGame(game)

                                        # Notify everyone who is playing that this player left
                                        for p in game.getPlayers():
                                            if p != currPlayer(s):
                                                sendStatus(p.getSocket(), 205)

                                        # Notify all observers as well
                                        for p in game.getObservers():
                                            sendStatus(p.getSocket(), 222, currPlayer(s).getUsername())

                                    sendStatus(currPlayer(s).getSocket(), 206)
                                    gameServer.logout(currPlayer(s))
                                    socketsToPlayers.pop(s, None)
                                    s.close()
                                    input.remove(s)
                            elif verb == "UNOBSERVE":
                                if not loggedIn(s):
                                    sendStatus(s, 401)
                                else:
                                    gid = int(arguments[0])
                                    cPlayer = currPlayer(s)

                                    if not cPlayer.isObserver():
                                        sendStatus(s, 421)

                                    game = cPlayer.getGame()

                                    if game.getId() != gid:
                                        retStr = str(gid) + ":" + str(game.getId())
                                        sendStatus(s, 430, retStr)
                                    else:
                                        game.removeObserver(cPlayer)
                                        cPlayer.endGame()
                                        sendStatus(s, 208)

                            elif verb == "HELP":
                                sendStatus(s, 212, resHelp())
                            elif verb == "BLANK":
                                sendStatus(s, 201)
                            elif verb == "COMMENT":
                                if not loggedIn(s):
                                    sendStatus(s, 401)
                                else:
                                    cPlayer = currPlayer(s)
                                    if cPlayer.canStartNewGame():
                                        sendStatus(s, 425)
                                    else:
                                        game = cPlayer.getGame()
                                        players = []

                                        players.append(game.getPlayers()[0])
                                        players.append(game.getPlayers()[1])
                                        players.extend(game.getObservers())

                                        retStr = "[ " + cPlayer.getUsername() + " ]:  "
                                        retStr += " ".join(arguments[0])
                                        retStr = retStr.replace("\n", "NEWLINE")

                                        for i in players:
                                            sendStatus(i.getSocket(), 230, retStr)

            else:  # sender wants to close the socket.
                if loggedIn(s):
                    # Get the game of the current player
                    game = currPlayer(s).getGame()

                    # If a game exists, end it
                    if game is not None and not currPlayer(s).isObserver():
                        gameServer.endGame(game)

                        # Notify everyone who is playing that this player left
                        for p in game.getPlayers():
                            if p != currPlayer(s):
                                sendStatus(p.getSocket(), 205)

                        # Notify all observers as well
                        for p in game.getObservers():
                            sendStatus(p.getSocket(), 222, currPlayer(s).getUsername())

                    gameServer.logout(currPlayer(s))
                    socketsToPlayers.pop(s, None)

                s.close()
                input.remove(s)

server.close()
