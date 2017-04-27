from enum import Enum


class Status(Enum):
    AVAILABLE = 1
    BUSY = 2


class Player:
    def __init__(self, username, socket):
        self.username = username
        self.status = Status.AVAILABLE
        self.socket = socket
        self.game = None
        self.symbol = None

    # Start a new game for the player
    def startGame(self, game, symbol):
        if not self.canStartNewGame():
            return

        self.game = game
        self.status = Status.BUSY
        self.symbol = symbol

    def endGame(self):
        self.game = None
        self.symbol = None
        self.status = Status.AVAILABLE

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
        return self.status == Status.AVAILABLE

    def sendData(self, data):
        self.socket.send(data)

    def getSocket(self):
        return self.socket