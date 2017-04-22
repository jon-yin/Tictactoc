CLIENT to SERVER protocol
=========================
Logging In:
-----------

Client sends

    LOGIN {username}

IF {username} is available server responds with

    STATUS 200

IF {username} is taken
Server responds with

    STATUS 422

Once logged in, Client can initiate the following:

Client sends
------------

    GAMES

IF Client is logged in, server responds with a comma separated list

    STATUS 200\n
    {gameId}:{player1}:{player2},{gameId}:{player1}:{player2},...

IF Client not logged in, server responds with

    STATUS 401


Client sends
------------
    WHO

IF Client is logged in, server responds with a comma separated list

    STATUS 200\n
    {player1},{player2},{player3},...

IF Client not logged in, server responds with

    STATUS 401

Client sends
------------

    PLAY {player}

IF Client is logged in, server responds with

    STATUS 200

IF Client not logged in, server responds with

    STATUS 401

IF Client is already in a game, server responds with

    STATUS 403

If player not found, server responds with

    STATUS 404

If player is busy, server responds with

    STATUS 422

IF player is the same person as the client, server responds with

    STATUS 400

Client sends
------------

    PLACE {move}

IF Client not logged in, server responds with

    STATUS 401

IF Client has not started a game, server responds with

    STATUS 400

IF it is not the Client's turn, server responds with

    STATUS 403

IF the move is not properly formatted {1-9}, server responds with

    STATUS 422

IF the move is not legal, server responds with

    STATUS 409

IF the move is legal and it is the client's turn, server responds with

    STATUS 200

**--> Server then sends to both clients**

    STATUS 201\n
    {player}:{move}

**--> IF the move won them the game, server responds again with**

    STATUS 202\n
    {winning player}


Client sends
------------

    EXIT

IF Client not logged in, server responds with

    STATUS 401

IF Client is logged in, server responds with

    STATUS 200

**--> IF Client was playing a game, server sends to other player**

    STATUS 205

