import select
import socket

from GameServer import GameServer
from ServerProtocol import Protocol

host = 'localhost'
port = 50000
backlog = 5
maxsize = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(backlog)
input = [server, ]  # a list of all connections we want to check for data

running = 1

gameServer = GameServer()
socketsToPlayers = {}


def sendStatus(soc, code, message=None):
    codeStr = "STATUS " + str(code)

    if message is not None:
        codeStr += "\n" + message

    codeStr += "\r\n\r\n"

    soc.send(codeStr.encode())


# Defining Part 1 command line arguments.
# Help Command, send to connection socket all supported commands.
def resHelp(socket):
    retString = ""
    retString += "LIST OF AVAILABLE COMMANDS\n"
    retString += "help: Prints all available commands. SYNTAX: $help \n"
    retString += "login: Login to the server, allowing you to both play and communicate with other players. SYNTAX: $login SAMPLE_NAME \n"
    retString += "place: Make a move and place a symbol onto the board, accepts a value from 1-9. SYNTAX: $place 4\n"
    retString += "exit: Quit from the current game if any and exit from the server SYNTAX: $exit \n"
    socket.send(retString)


# Exit Command, close connection socket.
def exitCommand(socket):
    socket.send("Exiting from server\n")
    socket.close()


def loggedIn(s):
    return s in socketsToPlayers


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
                protocol = Protocol(data)
                error, error_status = protocol.getError()

                if error:
                    sendStatus(s, error_status)
                else:
                    for message in protocol.getMessages():
                        error, error_status = message.getError()

                        if error:
                            sendStatus(s, error_status)
                        else:
                            verb, arguments = message.getInfo()

                            if verb == "LOGIN":
                                status, player = gameServer.login(arguments[0], s)

                                if status:
                                    sendStatus(s, 200)
                                    socketsToPlayers[s] = player
                                else:
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

                                    if toPlayer is None:
                                        sendStatus(s, 404)
                                    elif cPlayer == toPlayer:
                                        sendStatus(s, 409)
                                    else:
                                        status = gameServer.startNewGame(cPlayer, toPlayer)

                                        if status:
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

                                    if game is None:
                                        sendStatus(s, 400)
                                    else:
                                        players = game.getPlayers()

                                        if game.isTurn(cPlayer.getSymbol()):
                                            if game.makeMove(arguments[0], cPlayer.getSymbol()):
                                                sendStatus(s, 200)

                                                rstr = cPlayer.getUsername() + ":" + str(arguments[0])
                                                sendStatus(players[0].getSocket(), 201, rstr)
                                                sendStatus(players[1].getSocket(), 201, rstr)

                                                if game.isOver()[0]:
                                                    ret, loser = game.isOver()
                                                    winningPlayer = players[0]

                                                    if ret == players[1].getSymbol():
                                                        winningPlayer = players[1]

                                                    sendStatus(players[0].getSocket(), 202, winningPlayer.getUsername())
                                                    sendStatus(players[1].getSocket(), 202, winningPlayer.getUsername())

                                                    gameServer.endGame(game)
                                            else:
                                                sendStatus(s, 411)
                                        else:
                                            sendStatus(s, 406)

            else:  # sender wants to close the socket.
                if loggedIn(s):
                    gameServer.logout(currPlayer(s))
                    socketsToPlayers.pop(s, None)

                s.close()
                input.remove(s)

server.close()
