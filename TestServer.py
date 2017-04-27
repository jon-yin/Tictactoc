from ServerProtocol import Protocol

message = "WHO"

protocol = Protocol(message)
error, error_status = protocol.getError()


def sendStatus(code, message=None):
    codeStr = "STATUS " + str(code)

    if message is not None:
        codeStr += "\n" + message

    print(codeStr)


if error:
    sendStatus(error_status)
else:
    verb, arguments = protocol.getInfo()
    print(verb)
    print(arguments)
