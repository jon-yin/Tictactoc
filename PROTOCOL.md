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

    STATUS 250\n
    {gameId}:{player1}:{player2},{gameId}:{player1}:{player2},...

IF Client not logged in, server responds with

    STATUS 401


Client sends
------------
    WHO

IF Client is logged in, server responds with a comma separated list

    STATUS 251\n
    {player1}:{status},{player2}:{status},{player3}:{status},...

IF Client not logged in, server responds with

    STATUS 401

Client sends
------------

    PLAY {player}

IF Client is logged in, server responds with

    STATUS 200

**--> Server sends to {player}**

    STATUS 210\n
    {client name}

IF Client not logged in, server responds with

    STATUS 401

IF Client is already in a game, server responds with

    STATUS 403

If player not found, server responds with

    STATUS 404

If player is busy, server responds with

    STATUS 423

IF player is the same person as the client, server responds with

    STATUS 409

Client sends
------------

    PLACE {move}

IF Client not logged in, server responds with

    STATUS 401

IF Client has not started a game, server responds with

    STATUS 400

IF it is not the Client's turn, server responds with

    STATUS 406

IF the move is not properly formatted {1-9}, server responds with

    STATUS 424

IF the move is not legal, server responds with

    STATUS 411

IF the move is legal and it is the client's turn, server responds with

    STATUS 200

**--> Server then sends to both clients**

    STATUS 201\n
    {player}:{move}

**--> IF the move won them the game, server responds again with**

    STATUS 202\n
    {winning player}

**--> IF the move triggered a draw, server responds again with**

    STATUS 203

Client sends
------------

    EXIT

IF Client not logged in, server responds with

    STATUS 401

IF Client is logged in, server responds with

    STATUS 200

**--> IF Client was playing a game, server sends to other player**

    STATUS 205

**--> Server sends to client it is safe to exit**

    STATUS 206

Client sends
------------

    HELP

Server responds with

    STATUS 212\n
    {{help string}}
    
Client sends
------------

    OBSERVE {game id}

IF Client not logged in, server responds with

    STATUS 401
    
IF Client is playing a game, server responds with

    STATUS 408
    
IF Game does not exist, server responds with

    STATUS 406
    
Server sends if successful 

    STATUS 220\n
    {message}
    
Client sends
------------

    UNOBSERVE {game id}

IF Client not logged in, server responds with

    STATUS 401
    
IF Client is not observing a game, server responds with

    STATUS 421
    
IF Game does not exist, server responds with

    STATUS 430
    
Server sends if successful 

    STATUS 208
    
Client sends
------------

    COMMENT {comment}

IF Client not logged in, server responds with

    STATUS 401
    
IF Client is not observing a game, server responds with

    STATUS 425
    
**--> Server sends to clients observing and playing the game**

    STATUS 230\n
    {message}
    
       