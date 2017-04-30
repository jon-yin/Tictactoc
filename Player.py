class Player:
    def __init__(self, username, socket):
        self.username = username
        self.status = 1
        self.socket = socket
        self.game = None
        self.symbol = None

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