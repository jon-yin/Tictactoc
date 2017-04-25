import select
import socket
import sys

host = 'localhost'
port = 50000
backlog = 5
maxsize = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(backlog)
input = [server, ]  # a list of all connections we want to check for data

running = 1

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
                print('%s received from %s' % (data, s.getsockname()))

                # Uncomment below to echo the recv'd data back
                # to the sender... loopback!
                # s.send(data)
            else:  # if recv() returned NULL, that usually means the sender wants
                # to close the socket.
                s.close()
                input.remove(s)

server.close()
