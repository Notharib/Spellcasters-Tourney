import pygame
import pygame.freetype 
import time
import threading
import socket
import json
import random
import requests
import math

from menuScreens import gameStart, characterBuilder
from gameLogic import getDirection, data_handling
from arenaHandling import Platform, onPlat, platformInfo
from clientLogger import Logger
from Leaderboard import *
from Elements import *
from Casters import *
from projectiles import ProjectileGroup, Bullet, ConeAttack, generateCooldown


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
    def __init__(self,IPToConnectTo, socket=50000):
        self.__HOST = IPToConnectTo #String
        self.__PORT = socket #Integer
        self.playerID = None #Integer
        self.__socket = None #Object?
        self.__noOfPlatforms = 0 #Integer
        self.__waiting = None #Bool
        self.__playing = None #Bool
        self.__endGameData = None #Dict
        self.__clientPlayer = None #String?
        self.__leaderBoard = None #Object
        self.__lastMessageSent = time.time() #Float
        self.__recvMsg: bool = False
        self.__online: bool = False
        self.__sentMsg: bool = False


    '''
    Name: connect
    Parameters: None
    Returns: None
    Purpose: Connects the client object to the server, and then creates a Thread obejct that
    ensures that the server continuously listens for data from the server
    '''
    def connect(self):
        print(self.__HOST, self.__PORT)

        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((self.__HOST, self.__PORT))
            threading.Thread(target=self.listen).start()
            self.__online = True
        except ConnectionError as e:
            self.stopConn()
            logger.addToLog(e)

    
    def stopConn(self) -> None:
        '''
        Name: stopConn
        Parameters: None
        Returns: None
        Purpose: Ends the connection
        '''
        self.__socket.shutdown()
        self.__online = False

    '''
    Name: sendData
    Parameters: message: dictionary
    Returns: None
    Purpose: Converts the dictionary into JSON, and then encodes it and send the data to the server
    '''
    def sendData(self,message: dict) -> None:
        strMessage: str = json.dumps(message)
        self.__socket.send(strMessage.encode())
        self.__sentMsg = True

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
                    messageQueue = data_handling(data.decode())
                    
                    if not self.__recvMsg:
                        self.__recvMsg

                    if messageQueue is not None:
                        while not messageQueue.is_empty():
                            msg = messageQueue.dequeue()
                            if msg is not None:
                                self.__messageHandling(msg)
                            
                except json.JSONDecodeError as err:
                    print(data.decode())
                    logger.addToLog(err)
                    print("JSON Syntax Error:", err)
                
                except ConnectionError as e:
                    self.stopConn()
                    logger.addToLog(e)

    '''
    Name: __messageHandling
    Parameters: msg: dict
    Returns: None
    Purpose: Handles each indiviual message
    '''
    def __messageHandling(self, msg: dict) -> None:
        if msg["type"] == "leaderGet":
            self.setLeaderBoard(msg["data"])

        if msg["type"] == "playerID":
            print("client player created")
            self.playerID = msg["data"]["playerID"]
            addCharacter(msg["data"])

        if msg["type"] == "playerJoin":
            print("external player added")
            addCharacter(msg["data"])

        if msg["type"] == "fire":
            self.__projectileFired(msg["data"])
            
        if msg["type"] == "movement":
            self.__playerMoved(msg["data"])

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
            clPlData = {
                "playerID": msg["data"]["playerID"],
                "positionList": msg['data']['positionList'],
                'colourTuple': msg['data']['colourTuple']
            }
            addCharacter(clPlData)
            for player in list(msg["data"]["otherPlayersInfo"].keys()):
                playerData = msg["data"]["otherPlayersInfo"][player]
                playerData["playerID"] = player
                addCharacter(playerData)

            iterator = 0
            for platform in msg['data']['platformsPos']:
                createPlatform({'position':platform,'size':[20,500],'platformNo':iterator})
                iterator += 1

        if msg["type"] == "endGame":
            self.__playing = False
            self.__endGameData = msg["data"]

        if msg["type"] == "brokenPlayer":
            self.__kickBrokenPlayer(msg["data"])

        if msg["type"] == "MOVELEGAL":
            self.__clientPlayer.legalMove()
        if msg["type"] == "MOVENOTLEGAL":
            self.__clientPlayer.illegalMove()


    def __kickBrokenPlayer(msgData: int) -> None:
        '''
        Name:__kickBrokenPlayer
        Parameters: msgData:int
        Returns: None
        Purpose: To remove any broken players from the
        players sprite group
        '''
        playerSprites: list = players.sprites()
        for i in range(len(players.sprites())):
            if playerSprites[i].getPlayerID() == msgData:
                brokenPlayer = playerSprites[i]
        
        players.remove(brokenPlayer)
            
        


    '''
    Name: __projectileFired
    Parameters: msgData: dict
    Returns: None
    Purpose: Handles a projectile being fired by an external client
    '''
    def __projectileFired(self, msgData: dict) -> None:
        if msgData["casterType"] == "Druid":
            bullets.add(Bullet(msgData["spawnPoint"],msgData["direction"], msgData["playerID"], msgData["elementType"]))
        elif msgData["casterType"] == "Wizard":
            bullets.add(ConeAttack(msgData["spawnPoint"], msgData["playerID"], msgData["elementType"]))

    '''
    Name: __playerMoved
    Parameters: msgData: dict
    Returns: None
    Purpose: Handles an external player moving
    '''
    def __playerMoved(self, msgData) -> None:
        if len(players.sprites()) == 2:
            movedPlayer = players.sprites()[1]
        else:
            iteration = 0
            # print(players.sprites())
            for player in players.sprites():
                if player.getPlayerID() == msgData["playerID"]:
                    # print("found moved player")
                    movedPlayer = player
                    break
        if msgData["direction"] == "y":
            movedPlayer.rect.y = msgData["movedTo"]
        elif msgData["direction"] == "x":
            movedPlayer.rect.x = msgData["movedTo"]

    '''
    Name: tellServerDisconn
    Parameters: None
    Returns: None
    Purpose: Tells the server that this client wants to disconnect
    '''
    def tellServerDisconn(self):
        msgDict = {"type":"disconn", "data":{"playerID":self.playerID}}
        self.sendData(msgDict)

    #Getters and Setters

    '''
    Name: getRecvMsg
    Parameters: None
    Returns: bool
    Purpose: Getter for the recvmsg variable
    '''
    def getRecvMsg(self) -> bool:
        return self.__recvMsg

    def getSentMsg(self) -> bool:
        '''
        Name: getSentMsg
        Parameters: None
        Returns: bool
        Purpose: Getter for the sentMsg
        variable
        '''
        return self.__sentMsg

    '''
    Name: getOnline
    Parameters: None
    Returns: bool
    Purpose: Getter for the online variable
    '''
    def getOnline(self) -> bool:
        return self.__online

    '''
    Name: setLeaderBoard
    Parameters: leaderboard:dictionary
    Returns: None
    Purpose: Setter for the leaderboard variable
    '''
    def setLeaderBoard(self,leaderboard):
        self.__leaderBoard = leaderboard

    '''
    Name: enableWaiting
    Parameters: None
    Returns: None
    Purpose: Setter for the waiting variable
    '''
    def enableWaiting(self):
        self.__waiting = True

    '''
    Name: setClientPlayer
    Parameters: clPl: object
    Returns: None
    Purpose: Setter for the clientPlayer variable
    '''
    def setClientPlayer(self, clPl):
        self.__clientPlayer = clPl

    '''
    Name: waitingOver
    Parameters: None
    Returns: None
    Purpose: Setter for the waiting variable 
    '''
    def waitingOver(self):
        self.__waiting = False

    '''
    Name: checkWaiting
    Parameters: None
    Returns: self.__waiting
    Purpose: Getter for the waiting variable
    '''
    def checkWaiting(self):
        return self.__waiting

    '''
    Name: enablePlaying
    Parameters: None
    Returns: None
    Purpose: Setter for the playing variable
    '''
    def enablePlaying(self):
        self.__playing = True

    '''
    Name: playingOver
    Parameters: None
    Returns: None
    Purpose: Setter for the playing variable
    '''
    def playingOver(self):
        self.__playing = False

    '''
    Name: checkPlaying
    Parameters: None
    Returns: self.__playing
    Purpose: Getter for the playing variable
    '''
    def checkPlaying(self):
        return self.__playing

    '''
    Name: getEndGameData
    Parameters: None
    Returns: self.__endGameData
    Purpose: Getter for the endGameData variable
    '''
    def getEndGameData(self):
        return self.__endGameData

'''
Name: addCharacter
Parameters: data:dictionary
Returns: None
Purpose: Adds a Character object to the players pygame sprite group
'''
def addCharacter(data):
    players.add(Character(data["positionList"],data["colourTuple"],data["playerID"]))
    print("Player created!")

'''
Name: createBullet
Parameters: data:dictionary
Returns: None
Purpose: Adds a Bullet object to the bullets pygame sprite group
'''
def createBullet(data):
    bullets.add(Bullet(data["spawnPoint"],data["direction"],data["playerOrg"]))

'''
Name: createPlatform
Parameters: data:dictionary
Returns: None
Purpose: Adds a Platform object to the platforms pygame sprite group
'''
def createPlatform(data):
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
    def __init__(self, position, colour, playerID):
        super().__init__()
        self.height = 40
        self.width = 40
        self.X = position[0]
        self.Y = position[1]
        self.HP = 100
        self.colour = colour
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(colour)
        pygame.draw.rect(self.image,self.colour, [self.X, self.Y, self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y
        self.__playerID = playerID
        self.lastPos = [self.X,self.Y]
        self.lastLegalPos = self.lastPos
        self.collided = False
        self.__lastAttackTime = time.time()
        self.__regeneration: int = lambda t: round(math.exp(t // 4))
        self.__timeOfLastHit: float = time.time()
        self.__Element = None
        self.__Caster = None
        self.__OnFire: bool = False
        self.__attackCooldown: int|None = None
        self.__falling = True
        self.__timeFalling = time.time()
        self.__gravitySet: float = lambda t:  0.5 * 9,81 * t

    '''
    Name: update
    Parameters: None
    Returns: None
    Purpose: Updates certain variables each tick
    '''
    def update(self) -> None:
        tim = time.time()
        updTime = tim - self.__timeOfLastHit
        
        if self.HP != 100 and self.HP < 100 and not self.__OnFire:
            self.HP += self.__regeneration(updTime)
        if self.HP > 100:
            self.HP = 100
        
        if self.__OnFire:
            if updTime >= 5:
                self.__HP -= 5
                self.__timeOfLastHit = tim
                self.__OnFire = False
            elif updTime % 1 == 0:
                self.__HP -= 5
    '''
    Name: takeDamage
    Parameters: damage: int, fireEl: bool
    Returns: None
    Purpose: Setter for the client's health
    '''
    def takeDamage(self, damage: int, fireEl: bool = False) -> None:
        self.__HP -= damage
        self.__onFire = fireEl

        if self.__HP <= 0:
            self.rect.x = self.X
            self.rect.y = self.Y
            self.__HP = 100
            requests.post(url="http://127.0.0.1:5000/publicLeaderUpd", json={"playerID":self.__playerID})
        else:
            self.__timeOfLastHit = time.time()

    '''
    Name: setCaster
    Parameters: caster:str
    Returns: None
    Purpose: Setter for the Character Caster
    '''
    def __setCaster(self, caster: str) -> None:
        if caster == "Wizard":
            self.__Caster = Wizard()
        elif caster == "Druid":
            self.__Caster = Druid()
        else:
            raise ValueError(f"Internal Value Error: Incorrect Caster Type ({caster})")

    '''
    Name: setElement
    Parameters: element: str
    Returns: None
    Purpose: Setter for the Character Element
    '''
    def __setElement(self, element: str) -> None:
        if element == "Water":
            self.__Element = Water()
        elif element == "Fire":
            self.__Element = Fire()
        elif element == "Earth":
            self.__Element = Earth()
        else:
            raise ValueError(f"Internal Value Error: Incorrect Element Type ({element})")
    
    '''
    Name: getPlayerID
    Parameters: None
    Returns: self.__playerID
    Purpose: Getter for the playerID variable
    '''
    def getPlayerID(self) -> int:
        return self.__playerID

    '''
    Name: UpdateCharacteristics
    Parameters: characteristics: dict
    Returns: None
    Purpose: Sets the character's characteristics
    '''
    def UpdateCharacteristics(self, characteristics: dict) -> None:
        element: str = characteristics["element"]
        caster: str = characteristics["caster"]

        self.__setElement(element)
        self.__setCaster(caster)

        self.__attackCooldown = generateCooldown(self.__Element.getType())


    '''
    Name: leaderboardReq
    Parameters: serverType:string, client:object, serverKey:None|string
    Returns: None
    Purpose: Setter for the lastLegalPos variable
    '''
    def leaderboardReq(self,serverType,client,serverKey=None):
        if serverType is not None:
            leaderboard = getLeaderboard(serverType, self.__playerID, serverKey, client)
            if leaderboard is not None:
                client.setLeaderBoard(leaderboard)
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
    def legalMove(self):
        self.lastLegalPos = self.lastPos

    '''
    Name: illegalMove
    Parameters: None
    Returns: None
    Purpose: Reacts to being told by the server that the last legal move was 
    actually illegal
    '''
    def illegalMove(self):
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
    def checkIfLegal(self,direction,amount, client):
        checkIfLegalDict = {"type": "legalCheck", "data":{"direction":direction, "amount":amount, "playerID":self.__playerID}}
        client.sendData(checkIfLegalDict)
        time.sleep(0.01)
        return True

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
                        moveMessage = {"type": "movement","data": {"playerID": self.__playerID, "direction": "y", "movedTo": self.rect.y, "collided":self.collided}}
                        cl.sendData(moveMessage)
                        time.sleep(0.01)
                        moveMessage = {"type": "movement","data": {"playerID": self.__playerID, "direction": "x", "movedTo": self.rect.x, "collided":self.collided}}
                        cl.sendData(moveMessage)
                        self.lastPos = [self.rect.x, self.rect.y]
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
                        moveMessage = {"type": "movement","data": {"playerID": self.__playerID, "direction": "y", "movedTo": self.rect.y, "collided":self.collided}}
                        cl.sendData(moveMessage)
                        time.sleep(0.01)
                        moveMessage = {"type": "movement","data": {"playerID": self.__playerID, "direction": "x", "movedTo": self.rect.x, "collided":self.collided}}
                        cl.sendData(moveMessage)
                        self.lastPos = [self.rect.x, self.rect.y]

        elif keys[pygame.K_UP] == True:
            legalMove = self.checkIfLegal("y", 4, cl)
            if legalMove:
                self.rect.y -= 4
                if self.rect.y < 0:
                    self.rect.y = 0
                else:
                    self.lastMoveMade = ["y",-4]
                    moveMessage = {"type":"movement", "data":{"playerID": self.__playerID, "direction":"y", "movedTo":self.rect.y, "collided":self.collided}}
                    cl.sendData(moveMessage)
                    self.lastPos = [self.rect.x, self.rect.y]
                    time.sleep(0.01)
        elif keys[pygame.K_RIGHT] == True:
            legalMove = self.checkIfLegal("x", -2, cl)
            if legalMove:
                self.rect.x += 2
                if self.rect.x > 800:
                    self.rect.x = 800 - self.rect.x
                else:
                    self.lastMoveMade = ["x", 2]
                    moveMessage = {"type": "movement","data": {"playerID": self.__playerID, "direction": "x", "movedTo": self.rect.x, "collided":self.collided}}
                    cl.sendData(moveMessage)
                    self.lastPos = [self.rect.x, self.rect.y]
                    time.sleep(0.01)
        elif keys[pygame.K_LEFT] == True:
            legalMove = self.checkIfLegal("x", 2, cl)
            if legalMove:
                self.rect.x -= 2
                if self.rect.x < 0:
                    self.rect.x = 0
                else:
                    self.lastMoveMade = ["x", -2]
                    moveMessage = {"type": "movement","data": {"playerID": self.__playerID, "direction": "x", "movedTo": self.rect.x, "collided":self.collided}}
                    cl.sendData(moveMessage)
                    self.lastPos = [self.rect.x, self.rect.y]
                    time.sleep(0.01)
    

    '''
    Name: fire
    Parameters: client:object
    Returns: None
    Purpose: Sends a message to ther server that the player has created a bullet object
    '''
    def fire(self, client) -> None:
        mouseKeys = pygame.mouse.get_pressed(3)

        currTime: float = time.time()
        
        if mouseKeys[0] and (currTime - self.__lastAttackTime >= self.__attackCooldown):
            #main attack
            elementType: str = self.__Element.getType()
            casterType: str = self.__Caster.getType()

            if casterType == "Wizard":
                spawnPoint: list[int] = [self.rect.x-20, self.rect.y]
                direction: int = 0
                bullets.add(ConeAttack(spawnPoint, self.__playerID, elementType))
            elif casterType == "Druid":
                spawnPoint: list[int] = [self.rect.x, self.rect.y]
                direction: list[int] = getDirection(self)
                bullets.add(Bullet(spawnPoint, direction, self.__playerID, elementType))
             
            self.__lastAttackTime = currTime
            self.__tellServerFire(spawnPoint, client, direction)
    
    '''
    Name: __tellServerFire
    Parameters: spawnPoint:list[int], client:object, direction: list[int]|None
    Returns: None
    Purpose: Sends a message to ther server that the player has created a bullet object
    '''
    def __tellServerFire(self, spawnPoint:list[int], client, direction: list[int]|int) -> None:
        msgDict = {
                    "type": "fire",
                    "data": {
                            "playerID": self.__playerID,
                            "casterType": self.__Caster.getType(),
                            "elementType": self.__Element.getType(),
                            "spawnPoint": spawnPoint,
                            "direction": direction
                        }
                }

        client.sendData(msgDict)
        
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
                #self.lastMoveMade = ["y", 1]
                moveMessage = {"type": "movement","data": {"playerID": self.__playerID, "direction": "y", "movedTo": self.rect.y}}
                cl.sendData(moveMessage)
                self.lastPos = [self.rect.x, self.rect.y]

'''
Name: publicGame
Parameters: screen:object, clock:object, players:object, bullets: object, char:dictionary
Returns: None
Purpose: Handles the data for the player to be able to play on the public server
'''
def publicGame(screen, clock, players, platforms, bullets, char, serverType):

    # Creates an instance of the client object and connects it to the server
    c = Client("127.0.0.1")
    c.connect()

    time.sleep(2)

    print(char)

    # After a certain amount of time has passed, the server will have sent all the neccessary information required
    # for the player to be able to join the server. And the first message that the server will send is the informaiton
    # that the client will need to create its own player, so this then sets the clientPlayer variable to the first object
    # in the players sprite group
    clientPlayer = players.sprites()[0]
    c.setClientPlayer(clientPlayer)

    clientPlayer.UpdateCharacteristics(char)

    time.sleep(1)

    # Runs the platformInfo functio, which will send data to the server with information about the platforms if
    # the player's playerID is 1
    platformInfo(platforms, c, clientPlayer)

    mainRunLoop(clientPlayer, screen,clock,platforms,bullets,char,c, serverType)

'''
Name: mainRunLoop
Parameters: screen:object, clock:object, players:object, bullets: object, char:dictionary, c:object
Returns: None
Purpose: Main run loop for the game
'''
def mainRunLoop(clientPlayer, screen, clock, platforms, bullets, char, c, serverType):
    leaderboard = pygame.sprite.Group()
    leaderboard.add(Leaderboard())


    running = True
    showLeader = False
    
    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True

    leaderText = ""
    leaderUpd = time.time()

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
            leaderboard.update(getLeaderboard(serverType))
            showLeader = True
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
                if pl.getPlayerID() != b.getPlayerOrigin() and pl == clientPlayer:
                    
                    if b.getElement() == "Fire":
                        clientPlayer.takeDamage(b.getDamage(), True)
                    else:
                        clientPlayer.takeDamage(b.getDamage())
                    
                    bullets.remove(b)

        bullets.update()
        if (time.time()-leaderUpd) >= 30:
            leaderboard.update(getLeaderboard(serverType))
            timeUpd = time.time()

        clientPlayer.update()
        clientPlayer.gravity(c, plat)
        clientPlayer.move(c, plat)
        clientPlayer.fire(c)

        platforms.draw(screen)
        bullets.draw(screen)
        players.draw(screen)
        
        if showLeader:
            leaderboard.draw(screen)
            f.render_to(screen,(200,25), leaderText, (0,0,0))

        clock.tick(60)
        pygame.display.update()
    exit()

if __name__ == '__main__':
    logger = Logger()

    try:
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
        bullets = ProjectileGroup()

        char = characterBuilder(screen)

        # Only runs the code below if the player decides to join the public server (private server functionality needs to be worked on)
        beginInfo = gameStart(screen)

        if beginInfo["type"] == "publicGame":
            publicGame(screen, clock, players, platforms, bullets, char, "public")

    except Exception as e:
        logger.addToLog(str(e))