from Player import Player
from TicTacTocBoard import TicTacTocBoard


class GameServer:
    def __init__(self):
        self.games = {}
        self.players = {}
        self.currGameId = 1

    # Login a player from a username
    def login(self, username, socket):
        if username in self.players:
            return False, None
        else:
            player = Player(username, socket)
            self.players[username] = player
            return True, player

    def logout(self, player):

        # TODO End ongoing game

        self.players.pop(player.getUsername(), None)

    # Get a particular player from a username
    def getPlayer(self, username):
        if username in self.players:
            return self.players[username]
        else:
            return None

    # Start a new game instance
    def startNewGame(self, player1, player2):
        if not player1.canStartNewGame() or not player2.canStartNewGame():
            return False

        game = TicTacTocBoard(player1, player2, self.currGameId)

        self.games[self.currGameId] = game
        self.currGameId += 1

        player1.startGame(game, "X")
        player2.startGame(game, "O")

        return True

    def endGame(self, game):
        self.games.pop(game.getId(), None)
        players = game.getPlayers()
        players[0].endGame()
        players[1].endGame()

    # Get an array of ongoing games
    def getGames(self):
        rGames = []

        for id, game in self.games.items():
            players = game.getPlayers()
            rGames.append([id, players[0].getUsername(), players[1].getUsername()])

        return rGames

    # Get an array of logged in players
    def getPlayers(self):
        rPlayers = []

        for username, player in self.players.items():
            rPlayers.append([username, player.getStatus()])

        return rPlayers
