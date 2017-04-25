from Player import Player
from TicTacTocBoard import TicTacTocBoard


class GameServer:
    def __init__(self):
        self.games = {}
        self.players = {}
        self.currGameId = 1

    # Login a player from a username
    def login(self, username):
        if username in self.players:
            return False
        else:
            player = Player(username)
            self.players[username] = player
            return True

    # Get a particular player from a username
    def getPlayer(self, username):
        if username in self.players:
            return self.players[username]
        else:
            return False

    # Start a new game instance
    def startNewGame(self, player1, player2):
        if not player1.canStartNewGame() or not player2.canStartNewGame():
            return False

        game = TicTacTocBoard(player1, player2)

        self.games[self.currGameId] = game
        self.currGameId += 1

        player1.startGame(game)
        player2.startGame(game)

        return True

    # Get an array of ongoing games
    def getGames(self):
        rGames = []

        for id, game in self.games.items():
            rGames.append([id, game.getPlayers()])

        return rGames

    # Get an array of logged in players
    def getPlayers(self):
        rPlayers = []

        for username, player in self.players.items():
            rPlayers.append([username, player.getStatus()])

        return rPlayers
