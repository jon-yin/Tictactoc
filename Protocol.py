from enum import Enum


Verbs = Enum("Verbs", "LOGIN GAMES WHO PLAYER PLACE EXIT")


class Protocol:
    def __init__(self, message):
        self.error = False
        self.error_status = None
        self.arguments = []

        if not message:
            self.error = True
            self.error_status = 500
            return

        tokens = message.split()
        token_len = len(tokens)
        verb = tokens[0]

        if token_len < 1:
            self.error = True
            self.error_status = 500
            return

        if verb == Verbs.LOGIN.name:
            if token_len != 2:
                self.error = True
                self.error_status = 500
                return

            self.verb = verb
            self.arguments.append(tokens[1])
        elif verb == Verbs.GAMES.name:
            if token_len != 1:
                self.error = True
                self.error_status = 500
                return

            self.verb = verb
        elif verb == Verbs.WHO.name:
            if token_len != 1:
                self.error = True
                self.error_status = 500
                return

            self.verb = verb
        elif verb == Verbs.PLACE.name:
            if token_len != 2:
                self.error = True
                self.error_status = 500
                return

            pos = int(tokens[1])

            if pos < 0 or pos > 9:
                self.error = True
                self.error_status = 422
                return

            self.verb = verb
            self.arguments.append(pos)
        elif verb == Verbs.EXIT.name:
            if token_len != 1:
                self.error = True
                self.error_status = 500
                return

            self.verb = verb
        else:
            self.error = True
            self.error_status = 500

    def getError(self):
        return self.error, self.error_status

    def getInfo(self):
        return self.verb, self.arguments
