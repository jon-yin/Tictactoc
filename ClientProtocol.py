from ProtocolMessage import ProtocolMessage


class Protocol:
    def __init__(self, message):

        self.messages = []
        self.error = False
        self.error_status = None

        if not message:
            self.error = True
            self.error_status = 500
            return

        for res in message.split("\r\n\r\n"):
            if not res:
                continue

            pr = ProtocolMessage()
            parts = res.split("\n")

            if len(parts) == 1:
                tokens = parts[0].split()
                token_len = len(tokens)

                if token_len < 2:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue

                if int(tokens[1]) == 200:
                    pr.setVerb("SUCCESS")
                elif int(tokens[1]) == 203:
                    pr.setVerb("GAMEDRAW")
                elif int(tokens[1]) == 205:
                    pr.setVerb("PLAYEREXIT")
                elif int(tokens[1]) == 206:
                    pr.setVerb("SAFEEXIT")
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
                else:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue
            elif len(parts) == 2:
                tokens = parts[0].split()
                token_len = len(tokens)

                if token_len < 2:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue

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
                    pr.setVerb("NEWGAME")
                    pr.appendArgument(parts[1])
                elif int(tokens[1]) == 201:
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
                    pr.setVerb("WONGAME")
                    pr.appendArgument(parts[1])
                elif int(tokens[1]) == 212:
                    pr.setVerb("HELPSTR")
                    pr.appendArgument(parts[1].replace("{n}", "\n"))
                else:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue
            else:
                pr.setError(True)
                pr.setErrorStatus(500)
                self.messages.append(pr)
                continue

            self.messages.append(pr)

    def getError(self):
        return self.error, self.error_status

    def getMessages(self):
        return self.messages
