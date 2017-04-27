#Class for the TicTacTocBoard which represents a 3x3 board. The board can add
#elements to the board and check if the game is still ongoing
class TicTacTocBoard:
    #Initializes the board.
    def __init__(self, player1, player2, id):
        self.board = [[None, None, None],[None,None,None],[None,None,None]]
        self.player1 = player1
        self.player2 = player2
        self.id = id
        self.notPlayersTurn = "X"

    def getPlayers(self):
        return self.player1, self.player2

    def canPlay(self, player):
        return player == self.player1 or player == self.player2

    def getId(self):
        return self.id

    def isTurn(self, player):
        return player != self.notPlayersTurn

    # This method will attempt to make a move and set a symbol onto the board.
    # Returns true if board move is successful(setting a move onto an empty square)
    # Returns false if board move is unsuccessful (already a space on it or an invalid range).   
    def makeMove(self, position, symbol):
        position -= 1
        #return false if position is outside of range.
        if (position < 0 or position > 8):
            return False
        item = self.board[position//3][position%3]
        #return false if cell is not free.
        if (not item == None):
            return False
        else:
            #Place marker on board, return true/
            self.board[position//3][position%3] = symbol
            self.notPlayersTurn = symbol
            return True
    # Determines if the game is over(i.e if 3 symbols in a row have been found)
    # Returns true and the losing symbol if the game is over
    # Returns false if the game is still ongoing
    def isOver(self):
        #Iterate over rows and cols first.
        for i in range(3):
            #Check if the three in a row are equal and that they are not empty.
            if self.board[i][0] == self.board[i][1] and self.board[i][0] == self.board[i][2] and (not self.board[i][0] == None):
                return (True,self.board[i][0])
            #Repeat for the columns
            if self.board[0][i] == self.board[1][i] and self.board[0][i] == self.board[2][i] and (not self.board[0][i] == None):
                return (True, self.board[0][i])
        #Check 2 diagonals
        if self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2] and (not self.board[0][0] == None):
            return (True, self.board[0][0])
        if self.board[0][2] == self.board[1][1] and self.board[0][2] == self.board[2][0] and (not self.board[0][2] == None):
            return (True, self.board[0][2])
        #No 3 in a row found, see if there exists an empty space on the board.
        return ((not self.checkEmpty()), None)

    #This method will check to see if there still exists a vacant cell.
    #Returns true if an empty cell exists.
    #Returns false if no empty cell exists. 
    def checkEmpty(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == None:
                    return True
        return False
    
    #A string representation of the board.
    def __str__(self):
        retString = ""
        for i in range(3):
            for j in range(3):
                if (self.board[i][j] == None):
                    retString += ". "
                else:
                    retString += self.board[i][j] + " "
            retString += "\n"
        return retString
