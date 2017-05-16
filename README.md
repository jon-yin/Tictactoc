**CSE310 Final Project**

**Group # 43**

**Members Cho Ki Bbum, Fieger Brandon, Yin Jonathan**



Protocol is defined in PROTOCOL.md

HOW TO PLAY

1) Open a terminal and run


    python server.py

2) Open another terminal and run


    python client.py localhost 50000

3) In the test client terminal, enter a username. Then you enter the following


    WHO
    GAMES
    PLAY {username}
    EXIT

4) Open another terminal and run


    python client.py

5) In the new terminal enter a username. Then you can start a game with the other player


    PLAY {first username}

    Note: You can only play another player if they are not busy (they aren't already in a game)

6) Then you can bounce back and forth between terminals and entering


    PLACE {num}

7a) To observe a game, you can enter


    OBSERVE {num}

    where num is the id of the game to observe. Game ids can be found using the GAMES command.
    Note you can only observe 1 game at a time and you must unobserve before observing a new game.

 b) To stop observing a game, you enter

    UNOBSERVE {num}

    where num is the id of the game you are observing.

8) You can comment to other people in the server using

    COMMENT {message}
    
    You must be playing or observing a game to comment.


PROTOCOL CODES USED:

    CODE NUMBER  |  DESCRIPTION
        200      |  LOGIN SUCCESSFUL
        201      |  BLANK INPUT
        203      |  GAME ENDED IN DRAW
        205      |  OTHER PLAYER EXITED
        201      |  MAKING A MOVE
        202      |  SOMEONE WON THE GAME
        206      |  EXITING
        208      |  UNOBSERVING FROM GAME
        210      |  STARTING NEW GAME
        212      |  HELP
        220      |  OBSERVING BOARD
        222      |  UNOBSERVING BOARD
        230      |  MAKING A COMMENT
        250      |  SENDING GAME LIST
        251      |  SENDING PLAYER LIST
        404      |  PLAYER NOT FOUND
        406      |  NOT YOUR TURN
        408      |  PLAYER IS BUSY
        409      |  ATTEMPTING TO PLAY YOURSELF
        410      |  GAME DOESN'T EXIST
        411      |  INVALID MOVE
        421      |  CAN'T UNOBSERVE IF NOT OBSERVING
        422      |  USERNAME ALREADY TAKEN
        425      |  CANNOT COMMENT IF NOT IN GAME
        430      |  NOT OBSERVING THIS GAME
        500      |  ERROR




