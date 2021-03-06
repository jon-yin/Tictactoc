from ProtocolMessage import ProtocolMessage

# Helper class to parse and format request messages into multiple protocol messages


class Protocol:
    def __init__(self, message):

        self.messages = []
        self.error = False
        self.error_status = None

        # Make sure our message has some data to parse
        if not message:
            self.error = True
            self.error_status = 500
            return

        # For each message in our request
        for res in message.split("\\r\\n\\r\\n"):
            if not res:
                continue

            pr = ProtocolMessage()

            tokens = res.split()
            token_len = len(tokens)
            verb = tokens[0]

            # Every message has to start with STATUS {} which is min token len 2
            if token_len < 1:
                pr.setError(True)
                pr.setErrorStatus(500)
                self.messages.append(pr)
                continue

            # Parse and format different types of verbs (actions)
            # Protocol scheme is outlined in PROTOCOL.md
            if verb == "LOGIN":
                if token_len != 2:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue

                pr.setVerb(verb)
                pr.appendArgument(tokens[1])
            elif verb == "GAMES":
                if token_len != 1:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue

                pr.setVerb(verb)
            elif verb == "WHO":
                if token_len != 1:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue

                pr.setVerb(verb)
            elif verb == "PLAY":
                if token_len != 2:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue

                pr.setVerb(verb)
                pr.appendArgument(tokens[1])
            elif verb == "OBSERVE":
                if token_len != 2:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue

                pr.setVerb(verb)
                pr.appendArgument(tokens[1])

            elif verb == "UNOBSERVE":
                if token_len != 2:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue

                pr.setVerb(verb)
                pr.appendArgument(tokens[1])

            elif verb == "PLACE":
                if token_len != 2:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue

                pos = int(tokens[1])

                if pos < 0 or pos > 9:
                    pr.setError(True)
                    pr.setErrorStatus(422)
                    self.messages.append(pr)
                    continue

                pr.setVerb(verb)
                pr.appendArgument(pos)
            elif verb == "EXIT":
                if token_len != 1:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue

                pr.setVerb(verb)
            elif verb == "HELP":
                if token_len != 1:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue

                pr.setVerb(verb)
            elif verb == "COMMENT":
                if token_len == 1:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue
                pr.setVerb(verb)
                pr.appendArgument(tokens[1:])
            elif verb == "BLANK":
                if token_len > 1:
                    pr.setError(True)
                    pr.setErrorStatus(500)
                    self.messages.append(pr)
                    continue
                pr.setVerb(verb)
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
