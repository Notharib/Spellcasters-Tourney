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
from logger import generateLogFile, addToLog
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
    Parameters: IPToConnectTo: integer, logFile: str socket: integer
    Returns: None
    Purpose: Constructor to set the initial values
    of the client object
    '''
    def __init__(self,IPToConnectTo: str, logFile: str, socket: int =50000) -> None:
        self.__HOST: str = IPToConnectTo #String
        self.__PORT: int = socket #Integer
        self.playerID: None|int = None #Integer
        self.__socket = None #Object?
        self.__noOfPlatforms: int = 0 #Integer
        self.__clientPlayer = None #String?
        self.__leaderBoard: None|Leaderboard = None #Object
        self.__lastMessageSent: float = time.time() #Float
        self.__recvMsg: bool = False
        self.__online: bool = False
        self.__sentMsg: bool = False
        self.__logPath: str = logFile


    '''
    Name: connect
    Parameters: None
    Returns: None
    Purpose: Connects the client object to the server, and then creates a Thread obejct that
    ensures that the server continuously listens for data from the server
    '''
    def connect(self) -> None:
        print(self.__HOST, self.__PORT)

        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((self.__HOST, self.__PORT))
            threading.Thread(target=self.listen).start()
            self.__online = True
        except ConnectionError as e:
            self.stopConn()
            addToLog(self.__logPath, "clientnetworkconn", e)

    
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
                    messageQueue = data_handling(data.decode(), self.__logPath)
                    
                    if not self.__recvMsg:
                        self.__recvMsg

                    if messageQueue is not None:
                        while not messageQueue.is_empty():
                            msg = messageQueue.dequeue()
                            if msg is not None:
                                self.__messageHandling(msg)
                            
                except json.JSONDecodeError as err:
                    print(data.decode())
                    addToLog(self.__log, "clientnetwork", e)
                
                except ConnectionError as e:
                    self.stopConn()
                    addToLog(self.__log, "clientnetwork", e)

    '''
    Name: __messageHandling
    Parameters: msg: dict
    Returns: None
    Purpose: Handles each indiviual message
    '''
    def __messageHandling(self, msg: dict) -> None:
        try:
            if msg["type"] == "leaderGet":
                self.setLeaderBoard(msg["data"])

            if msg["type"] == "playerID":
                print("client player created")
                self.playerID = msg["data"]["playerID"]
                Client.addCharacter(msg["data"], self.__logPath)

            if msg["type"] == "playerJoin":
                print("external player added")
                Client.addCharacter(msg["data"], self.__logPath)

            if msg["type"] == "fire":
                self.__projectileFired(msg["data"])
                
            if msg["type"] == "movement":
                self.__playerMoved(msg["data"])

            if msg["type"] == "createPlat":
                print("Created platform")
                self.__createPlatform(msg["data"])

            if msg["type"] == "disconn":
                players.remove(players.sprites()[msg["data"]["playerID"]])
                print("Player Disconnected")

            if msg["type"] == "endGame":
                self.__playing = False
                self.__endGameData = msg["data"]

            if msg["type"] == "brokenPlayer":
                self.__kickBrokenPlayer(msg["data"])

            if msg["type"] == "MOVELEGAL":
                self.__clientPlayer.legalMove()
            if msg["type"] == "MOVENOTLEGAL":
                self.__clientPlayer.illegalMove()
        except Exception as e:
            addToLog(self.__logPath, "clientmsghandling", e)

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
            Client.createBullet(msgData["spawnPoint"],msgData["direction"], msgData["playerID"], msgData["elementType"])
        elif msgData["casterType"] == "Wizard":
            Client.createCone(msgData["spawnPoint"], msgData["playerID"], msgData["elementType"])

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
            movedPlayer = Client.getPlayerPosfromID(msgData["playerID"])

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
    def tellServerDisconn(self) -> None:
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

    '''
    Name: getSentMsg
    Parameters: None
    Returns: bool
    Purpose: Getter for the sentMsg
    variable
    '''
    def getSentMsg(self) -> bool:
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
    def setLeaderBoard(self,leaderboard: dict) -> None:
        self.__leaderBoard = leaderboard

    '''
    Name: setClientPlayer
    Parameters: clPl: object
    Returns: None
    Purpose: Setter for the clientPlayer variable
    '''
    def setClientPlayer(self, clPl):
        self.__clientPlayer = clPl

    '''
    Name: createPlatform
    Parameters: data:dictionary
    Returns: None
    Purpose: Adds a Platform object to the platforms pygame sprite group
    '''
    def __createPlatform(self, data: dict) -> None:
        platforms.add(Platform(data['position'],data['size'],data['platformNo']))

    '''
    Name: addCharacter
    Parameters: data:dictionary
    Returns: None
    Purpose: Adds a Character object to the players pygame sprite group
    '''
    def addCharacter(self, data: dict) -> None:
        players.add(Character(data["positionList"],data["colourTuple"],data["playerID"], self.__logPath))
        print("Player created!")

    # Static Methods (Functions mainly used by the client class, but technically
    # have nothing to do with it beyond that)

    '''
    Name: createBullet
    Parameters: spawnPoint: list[int], playerID: int, direction: list[int], elementType: str
    Returns: None
    Purpose: Static method that adds a Bullet 
    object to the bullets pygame sprite group
    '''
    @staticmethod
    def createBullet(spawnPoint: list[int], playerID: int, direction: list[int], elementType: str) -> None:
        bullets.add(Bullet(spawnPoint, direction, playerID, elementType))

    '''
    Name: createCone
    Parameters: spawnPoint: list[int], playerID: int, elementType: str
    Returns: None
    Purpose: Static method that creates a ConeAttack object in 
    the bullets pygame sprite group
    '''
    @staticmethod
    def createCone(spawnPoint: list[int], playerID: int, elementType: str) -> None:
        bullets.add(ConeAttack(spawnPoint, playerID, elementType))
    
    '''
    Name: getPlayerPosfromID
    Parameters: playerID: int
    Returns: player: object
    Purpose: Gets the position of a playerID in the list of sprites
    '''
    @staticmethod
    def getPlayerPosfromID(playerID: int) -> any:
        for player in players.sprites():
            if player.getPlayerID() == msgData["playerID"]:
                return player
        
        raise Exception("PlayerID Doesn't Exist")


'''
Name: Character
Purpose: To manage data surrounding each player's character, and how to handle certain actions
'''
class Character(pygame.sprite.Sprite):
    '''
    Name: __init__
    Parameters: position:list, colour:tuple, playerID:integer, logPath: str
    Returns: None
    Purpose: Constructor to set the initial values
    of the character object
    '''
    def __init__(self, position: list, colour: tuple[int,int,int], playerID: int, logPath: str) -> None:
        super().__init__()
        self.height = 40
        self.width = 40
        self.X = position[0]
        self.Y = position[1]
        self.__HP = 100
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
        self.__timeOfLastHit: float = self.__lastAttackTime
        self.__Element = None
        self.__Caster = None
        self.__OnFire: bool = False
        self.__grounded: bool = False
        self.__attackCooldown: int|None = None
        self.__gravityEq: int = lambda t: 0.5 * 9.81 * t
        self.__fallTime: float = self.__lastAttackTime
        self.__clientPlayer: bool = False
        self.__logPath: str = logPath

    '''
    Name: update
    Parameters: None
    Returns: None
    Purpose: Updates certain variables each tick
    '''
    def update(self, cl) -> None:
        tim = time.time()
        updTime = tim - self.__timeOfLastHit
        
        if self.__HP != 100 and self.__HP < 100 and not self.__OnFire:
            self.__HP += self.__regeneration(updTime)
        if self.__HP > 100:
            self.__HP = 100
        
        if self.__OnFire:
            self.takeDamage(5, cl)
            
            if updTime >= 5:
                self.__timeOfLastHit = tim
                self.__OnFire = False
        
        if self.__grounded:
            if updTime >= 3:
                self.__grounded = False

    '''
    Name: charError
    Parameters: errorFunc: str, error: str
    Returns: None
    Purpose: Allows the log file to specify whether it was the client
    player that errored or an external player
    '''
    def __charError(self, errorFunc: str, error: str) -> None:
        if self.__clientPlayer:
            addToLog(self.__logPath, f"clpl{errorFunc}", error)
        else:
            addToLog(self.__logPath, f"extpl{errorFunc}", error)
    
    '''
    Name: takeDamage
    Parameters: damage: int, fireEl: bool
    Returns: None
    Purpose: Setter for the client's health
    '''
    def takeDamage(self, damage: int, cl, fireEl: bool = False, earthEl: bool = False) -> None:
        self.__HP -= damage
        self.__OnFire = fireEl
        self.__grounded = earthEl

        if self.__HP <= 0:
            self.__charDeath(cl)
        else:
            self.__timeOfLastHit = time.time()

    '''
    Name: __charDeath
    Parameters: cl: Client
    Returns: None
    Purpose: Handles what to do when a character dies
    '''
    def __charDeath(self, cl) -> None:
        self.rect.x = self.X
        self.rect.y = self.Y
        self.__HP = 100
        self.__OnFire = False
        requests.post(url="http://127.0.0.1:5000/publicLeaderUpd", json={"playerID":self.__playerID})
        
        for letter in [["y", self.rect.y], ["x", self.rect.x]]:
            moveMsg: dict = {
                "type": "movement",
                "data": {
                    "playerID", self.__playerID,
                    "direction", letter[0],
                    "movedTo", letter[1],
                    "collided", self.collided
                }
            }
            cl.sendData(moveMsg)
            time.sleep(0.01)

    '''
    Name: move
    Parameters: cl:object, keys:list[bool]|None
    Returns: None
    Purpose: Changes the position of the sprite position based upon what key is being pressed
    by a pre-determined amount
    '''
    def move(self, cl, keys: list[bool]|None = None):
        try:
            if not self.__grounded:
                if keys is None:
                    keys = pygame.key.get_pressed()

                if keys[pygame.K_UP] == True and keys[pygame.K_LEFT] == True:
                    legalMove = self.checkIfLegal("y",4, cl)
                    if legalMove:
                        self.__changeRect("y", 4, cl)
                        legalMove = self.checkIfLegal("x",2, cl)
                        
                        if legalMove:
                            self.__changeRect("x", 2, cl)

                elif keys[pygame.K_UP] == True and keys[pygame.K_RIGHT] == True:
                    legalMove = self.checkIfLegal("y", 4, cl)
                    if legalMove:
                        self.__changeRect("y", 4, cl)

                        legalMove = self.checkIfLegal("x", -2, cl)
                        if legalMove:
                            self.__changeRect("x", -2, cl)

                elif keys[pygame.K_UP] == True:
                    legalMove = self.checkIfLegal("y", 4, cl)
                    if legalMove:
                        self.__changeRect("y", 4, cl)

                elif keys[pygame.K_RIGHT] == True:
                    legalMove = self.checkIfLegal("x", 2, cl)
                    if legalMove:
                        self.__changeRect("x", 2, cl)
                
                elif keys[pygame.K_LEFT] == True:
                    legalMove = self.checkIfLegal("x", -2, cl)
                    if legalMove:
                        self.__changeRect("x", -2, cl)
        except Exception as e:
            self.__charError("move", e)
    
    '''
    Name: __changeRect
    Parameters: direction: str, amount: int, cl: Client
    Returns: None
    Purpose: Changes the character's internal rect
    '''
    def __changeRect(self, direction: str, amount: int, cl) -> None:
        if direction == "y" or direction == "x":
            if direction == "y":
                self.rect.y += amount
                movedTo: int = self.rect.y
            elif direction == "x":
                self.rect.x += amount
                movedTo: int = self.rect.x
            
            moveMessage: dict = {
                "type": "movement",
                "data": {
                    "playerID": self.__playerID,
                    "direction": direction, 
                    "movedTo": movedTo,
                    "collided": self.collided
                }
            }
            cl.sendData(moveMessage)
            self.lastPos = [self.rect.x, self.rect.y]
            time.sleep(0.01)
            self.__outOfBoundsCheck(cl)
        else:
            raise ValueError(f"Internal Rect Change Value, Expecgted direction to be 'x' or 'y', got {direction}")

    '''
    Name: __outOfBoundsCheck
    Parameters: None
    Returns: None
    Purpose: Checks if the character has moved out of bounds, and handles what to do if they have
    '''
    def __outOfBoundsCheck(self, cl) -> None:
        if self.rect.y >= 800:
            self.__charDeath(cl)
        elif self.rect.x + self.width < 0:
            self.__charDeath(cl)
        elif self.rect.x >= 800:
            self.__charDeath(cl)

    '''
    Name: gravity
    Parameters: cl:object
    Returns: None
    Purpose: Adjusts the position of the character rect if the player 
    is not on a platform
    '''
    def gravity(self, cl):
        timothy: float = time.time()
        if not self.collided:
            self.__changeRect("y", self.__gravityEq(timothy-self.__fallTime), cl)
        else:
            self.__fallTime = timothy

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
    def checkIfLegal(self, direction: str, amount: int, client) -> bool:
        checkIfLegalDict = {"type": "legalCheck", "data":{"direction":direction, "amount":amount, "playerID":self.__playerID}}
        client.sendData(checkIfLegalDict)
        time.sleep(0.01)
        return True

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
                Client.createCone(spawnPoint, self.__playerID, elementType)
            elif casterType == "Druid":
                spawnPoint: list[int] = [self.rect.x, self.rect.y]
                direction: list[int] = getDirection(self)
                Client.createBullet(spawnPoint, self.__playerID, direction, elementType)
             
            self.__lastAttackTime = currTime
            self.__tellServerFire(spawnPoint, client, direction)
    
    '''
    Name: __tellServerFire
    Parameters: spawnPoint:list[int], client:object, direction: list[int]|int
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

    # Getters and Setters

    '''
    Name: setClientPlayer
    Paramaters: None
    Returns: None
    Purpose: Sets the character's clientPlayer variable
    to True
    '''
    def setClientPlayer(self) -> None:
        self.__clientPlayer = True

    '''
    Name: getPos
    Parameters: None
    Returns: list[int]
    Purpose: Getter for the character's position
    '''
    def getPos(self) -> list[int]:
        return [self.rect.x, self.rect.y]

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
        try: 
            element: str = characteristics["element"]
            caster: str = characteristics["caster"]
            self.__setElement(element)
            self.__setCaster(caster)

            self.__attackCooldown = generateCooldown(self.__Element.getType())

        except Exception as e:
            self.__charError("updchar", e)


'''
Name: platformCollide
Parameters: platforms|object, players:object, clientPlayer:object
Returns: bool
Purpose: Platoform + player collision handling
'''
def platformCollide(platforms, players, clientPlayer) -> bool:
    # Sprite group collision handling; handles collisions between platforms and players
    collisions = pygame.sprite.groupcollide(platforms, players, False, False)
    for platform, player_list in collisions.items():
        for player in player_list:
            if player == clientPlayer:
                return True
    return False

'''
Name: platformCollide
Parameters: platforms|object, players:object, clientPlayer:object
Returns: bool
Purpose: Platoform + player collision handling
'''
def projectileCollide(bullets, players, clientPlayer):
    pHit = pygame.sprite.groupcollide(bullets, players, False, False)
    for b, p_list in pHit.items():
        for pl in p_list:
            if pl.getPlayerID() != b.getPlayerOrigin() and pl == clientPlayer:
                
                if b.getElement() == "Fire":
                    clientPlayer.takeDamage(b.getDamage(), fireEl=True)
                elif b.getElement() == "Earth":
                    clientPlayer.takeDamage(b.getDamage(), earthEl=True)
                
                bullets.remove(b)
    
    return bullets, clientPlayer


'''
Name: publicGame
Parameters: screen:object, clock:object, players:object, bullets: object, char:dictionary, serverType: str, logFile: str
Returns: None
Purpose: Handles the data for the player to be able to play on the public server
'''
def publicGame(screen, clock, players, platforms, bullets, char: dict, serverType: str, logFile: str) -> None:

    # Creates an instance of the client object and connects it to the server
    c = Client("127.0.0.1", logFile)
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

        clientPlayer.collided = platformCollide(platforms, players, clientPlayer)

        bullets, clientPlayer = projectileCollide(bullets, players, clientPlayer)

        bullets.update()
        if (time.time()-leaderUpd) >= 30:
            leaderboard.update(getLeaderboard(serverType))
            timeUpd = time.time()

        clientPlayer.update(c)
        clientPlayer.gravity(c)
        clientPlayer.move(c)
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
    logPath: str = generateLogFile("client")

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
        addToLog(logPath, "generalclient", e)