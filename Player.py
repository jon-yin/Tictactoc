# Class to represent a player. A player can play games, observe games
# Also has a socket, username and a status
# Status of 0 is busy observing, 1 is free, 2 is busy in game


class Player:
    def __init__(self, username, socket):
        self.username = username
        self.status = 1
        self.socket = socket
        self.game = None
        self.symbol = None

    # Determines if this player is an observer
    def isObserver(self):
        return self.status == 0

    # Observes a game for this player.
    def observeGame(self,game):
        self.game = game
        self.status = 0
        game.addObserver(self)

    # Start a new game for the player
    def startGame(self, game, symbol):
        if not self.canStartNewGame():
            return

        self.game = game
        self.status = 2
        self.symbol = symbol

    def endGame(self):
        self.game = None
        self.symbol = None
        self.status = 1

    def getUsername(self):
        return self.username

    # Get the status of the player
    def getStatus(self):
        return self.status

    def getGame(self):
        return self.game

    def getSymbol(self):
        return self.symbol

    # Can the player start a new game
    def canStartNewGame(self):
        return self.status == 1

    def sendData(self, data):
        self.socket.send(data)

    def getSocket(self):
        return self.socket
