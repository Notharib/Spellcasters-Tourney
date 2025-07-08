import pygame,pygame.freetype, time, threading, socket, json, random
from menuScreens import gameStart, characterBuilder, waiting
from gameLogic import Bullet, Platform, Leaderboard, getDirection, youDied, onPlat, platformInfo, getLeaderboard, Leaderboard, queue
from PrivateServer import Server

'''
Name: Client
Purpose: To interact with the server, and to modify the players' information on the game
as new data is sent/received from the server
'''
class Client:
    '''
    Name: __init__
    Parameters: IPToConnectTo: integer, socket: integer
    Returns: None
    Purpose: Constructor to set the initial values
    of the client object
    '''
    def __init__(self,IPToConnectTo:str, port: int=50000) -> None:
        self.__HOST: str = IPToConnectTo #String
        self.__PORT: int = port #Integer
        self.playerID: int|None = None #Integer
        self.__socket: socket.socket|None = None #Object? I forgot what I do with this icl
        self.__noOfPlatforms: int = 0 #Integer
        self.__waiting: bool|None = None #Bool
        self.__playing: bool|None = None #Bool
        self.__endGameData: dict|None = None #Dict
        self.__clientPlayer = None #String?
        self.__leaderBoard: dict|None = None #Dictionary?
        self.__lastMessageSent: float = time.time() #Float
        self.__messageQueue: queue = queue() #Queue


    '''
    Name: connect
    Parameters: None
    Returns: None
    Purpose: Connects the client object to the server, and then creates a Thread obejct that
    ensures that the server continuously listens for data from the server
    '''
    def connect(self) -> None:
        print(self.__HOST, self.__PORT)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__HOST, self.__PORT))
        threading.Thread(target=self.listen).start()
        threading.Thread(target=self.queueEmptying).start()

    '''
    Name: queueEmptying 
    Parameters: Self
    Returns: None
    Description: Empties the next message in the messageQueue
    '''
    def queueEmptying(self) -> None:
        while True:
            if not self.__messageQueue.isempty():
                sendValue: dict = self.__messageQueue.dequeue()
                strSendValue: str = json.dumps(sendValue)
                self.__socket.send(strSendValue.encode())
                self.__lastMessageSent = time.time()
                time.sleep(0.01)

    '''
    Name: sendData
    Parameters: message: dictionary
    Returns: None
    Purpose: Converts the dictionary into JSON, and then encodes it and send the data to the server
    '''
    def sendData(self,message: dict) -> None:
        if (time.time() - self.__lastMessageSent) >= 0.01 and self.__messageQueue.is_empty():
            strMessage: str = json.dumps(message)
            self.__socket.send(strMessage.encode())
            self.__lastMessageSent = time.time()
        else:
            if message != self.__messageQueue.getBack():
                if not self.__messageQueue.is_full():
                    self.__messageQueue.enqueue(message)
                else:
                    raise Exception("Data Leak Error: Unique Message Not Sent to Server due to Queue issues")

    '''
    Name: listen
    Parameters: None
    Returns: None
    Purpose: Ran through a Thread object, it listens for data being sent by the server,
    and then handles what to do with it
    '''
    def listen(self) -> None:
        global clientPlayer
        while True:
            data = self.__socket.recv(1024)
            if not data:
                break
            else:
                try:
                    msg: dict = dict(json.loads(data.decode()))

                    if msg["type"] == "leaderGet":
                        self.setLeaderBoard(msg["data"])

                    if msg["type"] == "playerID":
                        print("client player created")
                        self.playerID = msg["data"]["playerID"]
                        addCharacter(msg["data"])

                    if msg["type"] == "playerJoin":
                        print("external player added")
                        addCharacter(msg["data"])

                    if msg["type"] == "movement":
                        if len(players.sprites()) == 2:
                            movedPlayer: Character = players.sprites()[1]
                        else:
                            iteration: int = 0
                            # print(players.sprites())
                            for player in players.sprites():
                                if player.playerID == msg["data"]["playerID"]:
                                    # print("found moved player")
                                    movedPlayer: Character = player
                                    break
    #                    if msg["data"]["direction"] == "y":
    #                        movedPlayer.rect.y = msg["data"]["movedTo"]
    #                    elif msg["data"]["direction"] == "x":
    #                        movedPlayer.rect.x = msg["data"]["movedTo"]
                        movedPlayer.rect.y = msg["data"]["posY"]
                        movedPlayer.rect.x = msg["data"]["posX"]

                    if msg["type"] == "createPlat":
                        print("Created platform")
                        platforms.add(Platform([msg["data"]["positionX"], msg["data"]["positionY"]],[msg["data"]["sizeHeight"], msg["data"]["sizeWidth"]],self.__noOfPlatforms))
                        self.__noOfPlatforms += 1

                    if msg["type"] == "disconn":
                        players.remove(players.sprites()[msg["data"]["playerID"]])
                        print("Player Disconnected")

                    if msg["type"] == "beginGame":
                        self.__waiting = False
                        print(msg['data'])
                        # addCharacter(msg["data"])
                        clPlData: dict = {
                            "playerID": msg["data"]["playerID"],
                            "positionList": msg['data']['positionList'],
                            'colourTuple': msg['data']['colourTuple']
                        }
                        addCharacter(clPlData)
                        for player in list(msg["data"]["otherPlayersInfo"].keys()):
                            playerData = msg["data"]["otherPlayersInfo"][player]
                            playerData["playerID"] = player
                            addCharacter(playerData)

                        iterator: int = 0
                        for platform in msg['data']['platformsPos']:
                            createPlatform({'position':platform,'size':[20,500],'platformNo':iterator})
                            iterator += 1

                    if msg["type"] == "endGame":
                        self.__playing = False
                        self.__endGameData = msg["data"]

                    if msg["type"] == "MOVELEGAL":
                        self.__clientPlayer.legalMove()
                    if msg["type"] == "MOVENOTLEGAL":
                        self.__clientPlayer.illegalMove()

                except json.JSONDecodeError as err:
                    print(data.decode())
                    print("JSON Syntax Error:", err)

    '''
    Name: tellServerDisconn
    Parameters: None
    Returns: None
    Purpose: Tells the server that this client wants to disconnect
    '''
    def tellServerDisconn(self) -> None:
        msgDict: dict = {"type":"disconn", "data":{"playerID":self.playerID}}
        self.sendData(msgDict)

    #Getters and Setters

    '''
    Name: setLeaderBoard
    Parameters: leaderboard:dictionary
    Returns: None
    Purpose: Setter for the leaderboard variable
    '''
    def setLeaderBoard(self,leaderboard: dict) -> None:
        self.__leaderBoard = leaderboard

    '''
    Name: enableWaiting
    Parameters: None
    Returns: None
    Purpose: Setter for the waiting variable
    '''
    def enableWaiting(self) -> None:
        self.__waiting = True

    '''
    Name: setClientPlayer
    Parameters: clPl: Character
    Returns: None
    Purpose: Setter for the clientPlayer variable
    '''
    def setClientPlayer(self, clPl) -> None:
        self.__clientPlayer = clPl

    '''
    Name: waitingOver
    Parameters: None
    Returns: None
    Purpose: Setter for the waiting variable 
    '''
    def waitingOver(self) -> None:
        self.__waiting = False

    '''
    Name: checkWaiting
    Parameters: None
    Returns: self.__waiting: None|bool
    Purpose: Getter for the waiting variable
    '''
    def checkWaiting(self) -> None|bool:
        return self.__waiting

    '''
    Name: enablePlaying
    Parameters: None
    Returns: None
    Purpose: Setter for the playing variable
    '''
    def enablePlaying(self) -> None:
        self.__playing = True

    '''
    Name: playingOver
    Parameters: None
    Returns: None
    Purpose: Setter for the playing variable
    '''
    def playingOver(self) -> None:
        self.__playing = False

    '''
    Name: checkPlaying
    Parameters: None
    Returns: self.__playing
    Purpose: Getter for the playing variable
    '''
    def checkPlaying(self) -> bool:
        return self.__playing

    '''
    Name: getEndGameData
    Parameters: None
    Returns: self.__endGameData
    Purpose: Getter for the endGameData variable
    '''
    def getEndGameData(self) -> dict:
        return self.__endGameData

'''
Name: addCharacter
Parameters: data:dictionary
Returns: None
Purpose: Adds a Character object to the players pygame sprite group
'''
def addCharacter(data: dict) -> None:
    players.add(Character(data["positionList"],data["colourTuple"],data["playerID"]))
    print("Player created!")

'''
Name: createBullet
Parameters: data:dictionary
Returns: None
Purpose: Adds a Bullet object to the bullets pygame sprite group
'''
def createBullet(data: dict) -> None:
    bullets.add(Bullet(data["spawnPoint"],data["direction"],data["playerOrg"]))

'''
Name: createPlatform
Parameters: data:dictionary
Returns: None
Purpose: Adds a Platform object to the platforms pygame sprite group
'''
def createPlatform(data: dict) -> None:
    platforms.add(Platform(data['position'],data['size'],data['platformNo']))

'''
Name: Character
Purpose: To manage data surrounding each player's character, and how to handle certain actions
'''
class Character(pygame.sprite.Sprite):
    '''
    Name: __init__
    Parameters: position:list, colour:tuple, playerID:integer
    Returns: None
    Purpose: Constructor to set the initial values
    of the character object
    '''
    def __init__(self, position:list[int], colour:tuple[int], playerID:int) -> None:
        super().__init__()
        self.height: int = 40
        self.width: int = 40
        self.X: int = position[0]
        self.Y: int = position[1]
        self.HP: int = 10
        self.colour: tuple = colour
        self.image: pygame.Surface = pygame.Surface([self.width, self.height])
        self.image.fill(colour)
        pygame.draw.rect(self.image,self.colour, [self.X, self.Y, self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y
        self.playerID: int = playerID
        self.lastPos: list[int] = [self.X,self.Y]
        self.lastLegalPos: list[int] = self.lastPos
        self.collided: bool = False
        self.lastBulletFired: float = time.time()

    '''
    Name: leaderboardReq
    Parameters: serverType:string, client:object, serverKey:None|string
    Returns: None
    Purpose: Setter for the lastLegalPos variable
    '''
    def leaderboardReq(self,serverType: str,client: Client,serverKey: str|None = None) -> Client:
        if serverType is not None:
            leaderboard: dict = getLeaderboard(serverType, self.playerID, serverKey, client)
            if leaderboard is not None:
                client.setLeaderBoard(leaderboard)
                print(leaderboard)
                print(type(leaderboard))
                return client
            else:
                return client
        else:
            raise Exception("None Type Error: serverType should be string type value, not NoneType")

    '''
    Name: legalMove
    Parameters: None
    Returns: None
    Purpose: Setter for the lastLegalPos variable
    '''
    def legalMove(self) -> None:
        self.lastLegalPos = self.lastPos

    '''
    Name: illegalMove
    Parameters: None
    Returns: None
    Purpose: Reacts to being told by the server that the last legal move was 
    actually illegal
    '''
    def illegalMove(self) -> None:
        if (not onPlat(self,platforms)) and self.collided:
            self.lastPos = self.lastLegalPos
            self.rect.x = self.lastPos[0]
            self.rect.y = self.lastPos[1]
        else:
            self.legalMove()

    '''
    Name: checkIfLegal
    Parameters: direction: string, amount:integer, client:object
    Returns: boolean
    Purpose: Sends a request to the server to check if a move was legal
    '''
    def checkIfLegal(self,direction: str,amount: int, client: Client) -> bool:
        checkIfLegalDict = {"type": "legalCheck", "data":{"direction":direction, "amount":amount, "playerID":self.playerID}}
        client.sendData(checkIfLegalDict)
        time.sleep(0.01)
        return True

    '''
    Name: __moveMessage
    Parameters: client:Client
    Returns: None
    Purpose: Sends a message to the server with the new coordinates
    '''
    def __moveMessage(self, client: Client) -> None:
        moveMessage: dict = {"type":"movement", "data":{"playerID":self.playerID, "collided":self.collided, "posX":self.rect.x, "posY":self.rect.y}}
        client.sendData(moveMessage)

    '''
    Name: move
    Parameters: cl:object, platform:object
    Returns: None
    Purpose: Changes the position of the sprite position based upon what key is being pressed
    by a pre-determined amount
    '''
    def move(self, cl, platform):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] == True and keys[pygame.K_LEFT] == True:
            legalMove = self.checkIfLegal("y",4, cl)
            if legalMove:
                self.rect.y -= 4
                legalMove = self.checkIfLegal("x",2, cl)
                if legalMove:
                    self.rect.x -= 2
                    if self.rect.y < 0:
                        self.rect.y = 0
                    elif self.rect.x < 0:
                        self.rect.x = 0
                    else:
                        self.lastMoveMade = ["y", -4]
                        self.__moveMessage(cl)
        elif keys[pygame.K_UP] == True and keys[pygame.K_RIGHT] == True:
            legalMove = self.checkIfLegal("y", 4, cl)
            if legalMove:
                self.rect.y -= 4
                legalMove = self.checkIfLegal("x", -2, cl)
                if legalMove:
                    self.rect.x += 2
                    if self.rect.y < 0:
                        self.rect.y = 0
                    elif self.rect.x > 800:
                        self.rect.x = 800 - self.rect.x
                    else:
                        self.lastMoveMade = ["y", -4]
                        self.__moveMessage(cl)

        elif keys[pygame.K_UP] == True:
            legalMove = self.checkIfLegal("y", 4, cl)
            if legalMove:
                self.rect.y -= 4
                if self.rect.y < 0:
                    self.rect.y = 0
                else:
                    self.lastMoveMade = ["y",-4]
                    self.__moveMessage(cl)
        elif keys[pygame.K_RIGHT] == True:
            legalMove = self.checkIfLegal("x", -2, cl)
            if legalMove:
                self.rect.x += 2
                if self.rect.x > 800:
                    self.rect.x = 800 - self.rect.x
                else:
                    self.lastMoveMade = ["x", 2]
                    self.__moveMessage(cl)
        elif keys[pygame.K_LEFT] == True:
            legalMove = self.checkIfLegal("x", 2, cl)
            if legalMove:
                self.rect.x -= 2
                if self.rect.x < 0:
                    self.rect.x = 0
                else:
                    self.lastMoveMade = ["x", -2]
                    self.__moveMessage(cl)


    '''
    Name: fire
    Parameters: client:object
    Returns: None
    Purpose: Sends a message to ther server that the player has created a bullet object
    '''
    def fire(self, client):
        mouseKeys = pygame.mouse.get_pressed(3)
        if mouseKeys[0] and (time.time() - self.lastBulletFired) > 0.1:
            direction = getDirection(self)
            bullets.add(Bullet([self.rect.x,self.rect.y],direction,self))
            client.sendData({"type":"bullCreate","data":{"direction":direction,"spawnPoint":[self.rect.x+self.width,self.rect.y], "playerOrg":self.playerID}})

    '''
    Name: gravity
    Parameters: cl:object, platform:object
    Returns: None
    Purpose: Adjusts the position of the character rect if the player 
    is not on a platform
    '''
    def gravity(self, cl, platform):
        if not self.collided:
            self.rect.y += 1
            if self.rect.y > 800 - self.height:
                self.rect.y = 800 - self.height
            else:
                self.__moveMessage(cl)
                self.lastPos = [self.rect.x, self.rect.y]

'''
Name: publicGame
Parameters: screen:object, clock:object, players:object, bullets: object, char:dictionary, serverType:string
Returns: None
Purpose: Handles the data for the player to be able to play on the public server
'''
def publicGame(screen, clock, players, platforms, bullets, char,serverType):

    # Creates an instance of the client object and connects it to the server
    c = Client("127.0.0.1")
    c.connect()

    time.sleep(3)

    # After a certain amount of time has passed, the server will have sent all the neccessary information required
    # for the player to be able to join the server. And the first message that the server will send is the informaiton
    # that the client will need to create its own player, so this then sets the clientPlayer variable to the first object
    # in the players sprite group
    clientPlayer = players.sprites()[0]
    c.setClientPlayer(clientPlayer)

    # Runs the platformInfo functio, which will send data to the server with information about the platforms if
    # the player's playerID is 1
    platformInfo(platforms, c, clientPlayer)

    mainRunLoop(clientPlayer, screen,clock,platforms,bullets,char,c,serverType)

'''
Name: privateCreate
Parameters: screen:object, clock:object, players:object, bullets: object, char:dictionary, creationData:dictionary, serverType:string 
Returns: None
Purpose: Handles the data for the player to be able to play on a private server, if they are the one who is hosting it
'''
def privateCreate(screen, clock, players, platforms, bullets, char, creationData, serverType):
    # Creates an instance of the private server, and then initialises it, using a Thread to continue to have the server run in the background
    server = Server(creationData["noOfPlayers"],creationData["lengthOfGame"], [[random.randint(0,800),random.randint(0,800)] for i in range(3)])
    threading.Thread(target=server.start).start()

    # Creates an instance of the Client object, and then joins to the private server, based
    # off the fact the server will be hosted by the same machine you're joining on
    c = Client(socket.gethostbyname(socket.gethostname()),socket=50001)
    c.connect()

    # Begins the waiting loop, which continues to run until the amount of players that the host initially
    # put in has been reached
    waiting(c, screen, creationData)

    # The first object in the players sprite group will be this clients player, so this just sets it so that is the case
    clientPlayer = players.sprites()[0]
    c.setClientPlayer(clientPlayer)

    # Sends the private server the platforms rect information
    platformInfo(platforms, c, clientPlayer)

    time.sleep(0.1)

    # for player in players.sprites():
    #     print(player.playerID)

    mainRunLoop(clientPlayer, screen,clock,platforms,bullets,char,c, serverType)

'''
Name: privateJoin
Parameters: screen:object, clock:object, players:object, bullets: object, char:dictionary, creationData:dictionary, serverType:string 
Returns: None
Purpose: Handles joining a private server that someone else is hosting
'''
def privateJoin(screen, clock, players, platforms, bullets, char, creationData,serverType):

    # Creates a client object with the IP address given to the player by the API, and then connects that client to the server
    c = Client(creationData["IPAddress"], socket=50001)
    c.connect()

    print("Joined up to the private server!")

    # Wait loop that runs while the server is waiting for all the players to join
    waiting(c, screen, creationData)

    # After the wait loop is over, this players character will be at the front of the players sprite group sprites, so
    # this just turns that into a unique variable, to make handling it easier
    clientPlayer = players.sprites()[0]
    c.setClientPlayer(clientPlayer)

    time.sleep(0.1)

    mainRunLoop(clientPlayer, screen,clock,platforms,bullets,char,c,serverType)

def leaderBoardUpd(serverType, client):
    if serverType == "public":
        client.sendData({"type:leaderReq"})
        
'''
Name: mainRunLoop
Parameters: screen:object, clock:object, players:object, bullets: object, char:dictionary, c:object, serverType:string
Returns: None
Purpose: Main run loop for the game
'''
def mainRunLoop(clientPlayer, screen, clock, platforms, bullets, char, c, serverType):
    leaderboard = pygame.sprite.Group()
    leaderboard.add(Leaderboard())


    running = True
    showLeader = False
    lastLeaderStatus = False
    lastLeaderUpd = time.time()

    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True

    leaderText = ""

    # Run loop
    while running:

        clientPlayer.collided = False
        plat = None

        screen.fill(WHITE)

        tab = pygame.key.get_pressed()[pygame.K_TAB]
        if not tab:
            showLeader = False
            leaderText = ""
        else:
            if not lastLeaderStatus:
                leaderboard.update(getLeaderboard(serverType))
                showLeader = True
                leaderText = leaderboard.sprites()[0].getDisplayText()
            else:
                if (time.time()-lastLeaderUpd) >= 15:
                    leaderboard.update(getLeaderboard(serverType))
                    leaderText = leaderboard.sprites()[0].getDisplayText()

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                c.tellServerDisconn()
                exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                # mods = pygame.key.get_mods()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseKey = pygame.mouse.get_pressed(3)

        # Sprite group collision handling; handles collisions between platforms and players
        collisions = pygame.sprite.groupcollide(platforms, players, False, False)
        for platform, player_list in collisions.items():
            for player in player_list:
                if player == clientPlayer:
                    clientPlayer.collided = True

        # Sprite group collision handling; handles collisions between projectiles and players
        pHit = pygame.sprite.groupcollide(bullets, players, False, False)
        for b, p_list in pHit.items():
            for pl in p_list:
                if pl != b.playerOrigin:
                    pl.HP -= b.damage
                    pl = youDied(pl, screen)
                    bullets.remove(b)

        bullets.update()
        clientPlayer.gravity(c, plat)
        clientPlayer.move(c, plat)
        clientPlayer.fire(c)
        platforms.draw(screen)
        bullets.draw(screen)
        players.draw(screen)

        if showLeader:
            if not lastLeaderStatus:
                lastLeaderStatus = True
            #print(leaderText)
            leaderboard.draw(screen)
            f.render_to(screen,(200,25), leaderText, (0,0,0))
        if lastLeaderStatus and not showLeader:
            lastLeaderStatus = False
        
        clock.tick(60)
        pygame.display.update()
    exit()

if __name__ == '__main__':
    pygame.display.init()
    pygame.font.init()
    pygame.freetype.init()
    WINDOW_SIZE = (800, 800)

    RED = (250, 9, 1)
    GREEN = (2, 249, 0)
    BLUE = (0, 0, 240)
    PURPLE = (160, 32, 240)
    WHITE = (255,255,255)

    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    players = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    char = characterBuilder(screen)

    beginInfo = gameStart(screen)

    if beginInfo["type"] == "publicGame":
        publicGame(screen, clock, players, platforms, bullets, char, "public")

    if beginInfo["type"] == "privateCreate":
        privateCreate(screen, clock, players, platforms, bullets, char, beginInfo["data"],"private")

    if beginInfo["type"] == "privateJoin":
        privateJoin(screen, clock, players, platforms, bullets, char, beginInfo["data"], "private")
