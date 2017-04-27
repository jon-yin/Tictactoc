import select
import socket
import sys

from GameServer import GameServer
from Protocol import Protocol

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


def sendStatus(soc, code, message=None):
    codeStr = "STATUS " + str(code)

    if message is not None:
        codeStr += "\n" + message

    soc.send(codeStr)

#Defining Part 1 command line arguments.
#Help Command, send to connection socket all supported commands.
def resHelp(socket):
    retString = ""
    retString += "LIST OF AVAILABLE COMMANDS\n"
    retString += "help: Prints all available commands. SYNTAX: $help \n"
    retString += "login: Login to the server, allowing you to both play and communicate with other players. SYNTAX: $login SAMPLE_NAME \n"
    retString += "place: Make a move and place a symbol onto the board, accepts a value from 1-9. SYNTAX: $place 4\n"
    retString += "exit: Quit from the current game if any and exit from the server SYNTAX: $exit \n")
    socket.send(retString)
    
#Exit Command, close connection socket.
def exitCommand(socket):
    socket.send("Exiting from server\n")
    socket.close()


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
            data = s.recv(maxsize)

            if data:
                protocol = Protocol(data)
                error, error_status = protocol.getError()

                if error:
                    sendStatus(s, error_status)
                else:
                    verb, arguments = protocol.getInfo()
                    print(verb)
                    print(arguments)

                    # Uncomment below to echo the recv'd data back
                    # to the sender... loopback!
                    # s.send(data)
            else:  # if recv() returned NULL, that usually means the sender wants
                # to close the socket.
                s.close()
                input.remove(s)

server.close()
