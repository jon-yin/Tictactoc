from ProtocolMessage import ProtocolMessage


#Serves to error check  and parse server messages.
class Protocol:
    def __init__(self, message):

        self.messages = []
        self.error = False
        self.error_status = None

        #If no server response(no status code nor message, print an error)
        if not message:
            self.error = True
            self.error_status = 500
            return

        #Cuts off the very end of the message.
        for res in message.split("\r\n\r\n"):
            if not res:
                continue

            pr = ProtocolMessage()
            parts = res.split("\n")
            #Distinguish between two different types of messages, ones with status code only and ones with status code + message.
            if len(parts) == 1:
                tokens = parts[0].split()
                token_len = len(tokens)
                #Every message should be at least 2 tokens long.
                if token_len < 2:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue
                #Send appropriate message to client based on status code.
                if int(tokens[1]) == 200:
                    pr.setVerb("SUCCESS")
                elif int(tokens[1]) == 203:
                    pr.setVerb("GAMEDRAW")
                elif int(tokens[1]) == 205:
                    pr.setVerb("PLAYEREXIT")
                elif int(tokens[1]) == 206:
                    pr.setVerb("SAFEEXIT")
                elif int(tokens[1]) == 208:
                    pr.setVerb("UNOBSERVED")
                elif int(tokens[1]) == 422:
                    pr.setVerb("USERNAMETAKEN")
                elif int(tokens[1]) == 406:
                    pr.setVerb("NOTTURN")
                elif int(tokens[1]) == 411:
                    pr.setVerb("ILLEGALMOVE")
                elif int(tokens[1]) == 409:
                    pr.setVerb("PLAYYOURSELF")
                elif int(tokens[1]) == 404:
                    pr.setVerb("PLAYERNOTFOUND")
                elif int(tokens[1]) == 408:
                    pr.setVerb("BUSY")
                elif int(tokens[1]) == 414:
                    pr.setVerb("CANTPLACEOBS")
                elif int(tokens[1]) == 421:
                    pr.setVerb("NOOBSERVE")
                elif int(tokens[1]) == 425:
                    pr.setVerb("FREE")
                elif int(tokens[1]) == 201:
                    pr.setVerb("BLANK")

                else:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue
            #If server message also has an additional message.
            elif len(parts) == 2:
                tokens = parts[0].split()
                token_len = len(tokens)

                if token_len < 2:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue
                #Parse the gamelist sent by the server to allow easier processing by the client.
                if int(tokens[1]) == 250:
                    li = []
                    groups = parts[1].split(",")

                    for g in groups:
                        pieces = g.split(":")

                        if len(pieces) != 3:
                            continue

                        pieces[0] = int(pieces[0])

                        li.append(pieces)

                    pr.setVerb("GAMELIST")
                    pr.appendArgument(li)
                elif int(tokens[1]) == 251:
                    #Parse every player as well as their status.
                    li = []
                    groups = parts[1].split(",")

                    for g in groups:
                        pieces = g.split(":")

                        if len(pieces) != 2:
                            continue

                        pieces[1] = int(pieces[1])

                        li.append(pieces)

                    pr.setVerb("PLAYERLIST")
                    pr.appendArgument(li)
                elif int(tokens[1]) == 210:
                    #Initiate a new game.
                    pr.setVerb("NEWGAME")
                    pr.appendArgument(parts[1])
                elif int(tokens[1]) == 201:
                    #A player has made a move.
                    args = parts[1].split(":")

                    if len(args) != 2:
                        pr.setError(True)
                        pr.setErrorStatus(500)
                        self.messages.append(pr)
                        continue

                    pr.setVerb("NEWMOVE")
                    pr.appendArgument(args[0])
                    pr.appendArgument(int(args[1]))
                elif int(tokens[1]) == 202:
                    #Some player has won the game.
                    pr.setVerb("WONGAME")
                    pr.appendArgument(parts[1])
                elif int(tokens[1]) == 410:
                    #Client refers to a non-existant game
                    pr.setVerb("GAMEDOESNTEXIST")
                    pr.appendArgument(parts[1])
                elif int(tokens[1]) == 212:
                    #Client requests help string.
                    pr.setVerb("HELPSTR")
                    pr.appendArgument(parts[1].replace("{n}", "\n"))
                elif int(tokens[1]) == 220:
                    #Client recieves the status of a game it's observering
                    pr.setVerb("SENDBRD")
                    pr.appendArgument(parts[1])

                elif int(tokens[1]) == 222:
                    #Observer has exitted a game (not unobserved)
                    pr.setVerb("OBSEXIT")
                    pr.appendArgument(parts[1])
                elif int(tokens[1]) == 430:
                    #Observer refers to unobserving the wrong game.
                    pr.setVerb("WRNGGAME")
                    pr.appendArgument(parts[1])
                elif int(tokens[1]) == 230:
                    #Client recieves a comment from a player/observer.
                    pr.setVerb("COMMENT")
                    pr.appendArgument(parts[1])

                else:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue
            else:
                #If status code is none of the above, this means that this is an error.
                pr.setError(True)
                pr.setErrorStatus(500)
                self.messages.append(pr)
                continue

            self.messages.append(pr)

    def getError(self):
        return self.error, self.error_status

    def getMessages(self):
        return self.messages
