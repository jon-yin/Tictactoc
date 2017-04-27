class ProtocolMessage:
    def __init__(self):
        self.error = False
        self.error_status = None
        self.arguments = []
        self.verb = None

    def setError(self, error):
        self.error = error

    def setErrorStatus(self, error_status):
        self.error_status = error_status

    def setVerb(self, verb):
        self.verb = verb

    def appendArgument(self, argument):
        self.arguments.append(argument)

    def getError(self):
        return self.error, self.error_status

    def getInfo(self):
        return self.verb, self.arguments
