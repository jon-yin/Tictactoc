from enum import Enum

class Status(Enum):
    AVAILABLE = 1
    BUSY = 2

class Player:
	def __init__(self, username):
		self.username = username
		self.status = Status.AVAILABLE
		self.game = None
		
	# Start a new game for the player
	def startGame(self, game):
		if !self.canStartNewGame()
			return
			
		self.game = game
		self.status = Status.BUSY
		
	# Get the status of the player
	def getStatus(self):
		return self.status
		
	# Can the player start a new game
	def canStartNewGame(self):
		return self.status == Status.AVAILABLE
