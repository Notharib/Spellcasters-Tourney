import pygame,pygame.freetype, time, threading, socket, json, random
from menuScreens import gameStart, characterBuilder
from gameLogic import getDirection, youDied, onPlat, Bullet, Platform
from PrivateServer import Server

# Client class, not possible to modularise in current capacity due to how interlinked it is with the core code
class Client:
    def __init__(self,IPToConnectTo):
        self.__HOST = IPToConnectTo
        self.__PORT = 50000
        self.clientNo = None
        self.__socket = None
        self.__noOfPlatforms = 0
        self.__waiting = None
        self.__playing = None
        self.__endGameData = None
        self.__clientPlayer = None

    def connect(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__HOST, self.__PORT))
        threading.Thread(target=self.listen).start()

    # Sends whatever data is passed into the function to the server it is connected to
    def sendData(self,message):
        strMessage = json.dumps(message)
        self.__socket.send(strMessage.encode())

    # Listens for JSON formatted data from the server
    def listen(self):
        global clientPlayer
        while True:
            data = self.__socket.recv(1024)
            if not data:
                break
            else:
                try:
                    msg = dict(json.loads(data.decode()))

                    if msg["type"] == "clientNo":
                        print("client player created")
                        self.clientNo = msg["data"]["clientNo"]
                        addCharacter(msg["data"])
                    if msg["type"] == "playerJoin":
                        print("external player added")
                        addCharacter(msg["data"])
                    if msg["type"] == "movement":
                        if len(players.sprites()) == 2:
                            movedPlayer = players.sprites()[1]
                        else:
                            iteration = 0
                            for player in players.sprites():
                                if iteration == 0:
                                    pass
                                else:
                                    if player.characterNo == msg["data"]["playerNo"]:
                                        print("found moved player")
                                        movedPlayer = player
                                        break
                        if msg["data"]["direction"] == "y":
                            movedPlayer.rect.y = msg["data"]["movedTo"]
                        elif msg["data"]["direction"] == "x":
                            movedPlayer.rect.x = msg["data"]["movedTo"]

                    if msg["type"] == "createPlat":
                        print("Created platform")
                        platforms.add(Platform([msg["data"]["positionX"], msg["data"]["positionY"]],[msg["data"]["sizeHeight"], msg["data"]["sizeWidth"]],self.__noOfPlatforms))
                        self.__noOfPlatforms += 1
                    if msg["type"] == "disconn":
                        players.remove(players.sprites()[msg["data"]["clientNo"]])
                        print("Player Disconnected")

                    if msg["type"] == "beginGame":
                        self.__waiting = False
                        addCharacter(Character(msg["data"]["playerSpawnPoint"],msg["data"]["playerColour"],msg["data"]["playerNo"]))
                        for player in list(msg["data"]["otherPlayersInfo"].keys()):
                            playerData = msg["data"]["otherPlayersInfo"][player]
                            addCharacter(Character(playerData["spawnPoint"], playerData["colour"],player))
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

    def tellServerDisconn(self):
        msgDict = {"type":"disconn", "data":{"clientNo":self.clientNo}}
        self.sendData(msgDict)

    #Getters and Setters

    def enableWaiting(self):
        self.__waiting = True

    def setClientPlayer(self, clPl):
        self.__clientPlayer = clPl

    def waitingOver(self):
        self.__waiting = False

    def checkWaiting(self):
        return self.__waiting

    def enablePlaying(self):
        self.__playing = True

    def playingOver(self):
        self.__playing = False

    def checkPlaying(self):
        return self.__playing

    def getEndGameData(self):
        return self.__endGameData

# Adds a Player object to the players sprite group (potential to modularise?)
def addCharacter(data):
    players.add(Character(data["positionList"],data["colourTuple"],data["clientNo"]))
    print("Player created!")

# Adds a Bullet object to the bullets/projectiles sprite group
def createBullet(data):
    bullets.add(Bullet(data["spawnPoint"],data["direction"],data["playerOrg"]))

#
def clientData(collecting, t, passedData):
    while collecting:
        if t is not None:
            if t == "addCharacter":
                addCharacter(passedData)
                return False
            if t == "movement":
                if len(players.sprites()) == 2:
                    movedPlayer = players.sprites()[1]
                else:
                    iteration = 0
                    for player in players.sprites():
                        if iteration == 0:
                            pass
                        else:
                            if player.characterNo == passedData["playerNo"]:
                                print("found moved player")
                                movedPlayer = player
                                break
                if passedData["direction"] == "y":
                    movedPlayer.rect.y = passedData["movedTo"]
                elif passedData["direction"] == "x":
                    movedPlayer.rect.x = passedData["movedTo"]
                return False
            if t == "createPlat":
                platforms.add(Platform([passedData["positionX"], passedData["positionY"]],[passedData["sizeHeight"], passedData["sizeWidth"]], passedData["noOfPlats"]))
                return False
            if t == "disconn":
                players.remove(players.spites()[passedData["clientNo"]])
                return False
            if t == "bullCreate":
                bullets.add(Bullet(passedData["spawnPoint"],passedData["direction"]))
                return False
            if t == "legalMove":
                clientPlayer.legalMove()
                return False
            if t == "illegalMove":
                clientPlayer.illegalMove()

class Character(pygame.sprite.Sprite):
    def __init__(self, position, colour, playerNo):
        super().__init__()
        self.height = 40
        self.width = 40
        self.X = position[0]
        self.Y = position[1]
        self.HP = 10
        self.colour = colour
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(colour)
        pygame.draw.rect(self.image,self.colour, [self.X, self.Y, self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y
        self.characterNo = playerNo
        self.lastPos = [self.X,self.Y]
        self.lastLegalPos = self.lastPos
        self.collided = False

    def legalMove(self):
        self.lastLegalPos = self.lastPos

    def illegalMove(self):
        if (not onPlat(self,platforms)) and self.collided:
            self.lastPos = self.lastLegalPos
            self.rect.x = self.lastPos[0]
            self.rect.y = self.lastPos[1]
        else:
            self.legalMove()

    def checkClosestPlat(self):
        closestPlat = None
        closestPlatX = 0
        iteration = 0
        for platform in platforms.sprites():
            if iteration == 0:
                closestPlatX = platform.rect.x
                iteration += 1
            else:
                if closestPlatX > self.rect.x:
                    if platform.rect.x < closestPlatX and (platform.rect.x >= closestPlatX or platform.rect.x <= closestPlatX):
                        closestPlatX = platform.rect.x

    def checkIfLegal(self,direction,amount, client):
        checkIfLegalDict = {"type": "legalCheck", "data":{"direction":direction, "amount":amount, "clientNo":client.clientNo}}
        client.sendData(checkIfLegalDict)
        time.sleep(0.01)
        return True

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
                        moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "y", "movedTo": self.rect.y, "collided":self.collided}}
                        cl.sendData(moveMessage)
                        time.sleep(0.01)
                        moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x, "collided":self.collided}}
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
                        moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "y", "movedTo": self.rect.y, "collided":self.collided}}
                        cl.sendData(moveMessage)
                        time.sleep(0.01)
                        moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x, "collided":self.collided}}
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
                    moveMessage = {"type":"movement", "data":{"playerNo": self.characterNo, "direction":"y", "movedTo":self.rect.y, "collided":self.collided}}
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
                    moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x, "collided":self.collided}}
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
                    moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x, "collided":self.collided}}
                    cl.sendData(moveMessage)
                    self.lastPos = [self.rect.x, self.rect.y]
                    time.sleep(0.01)

    def fire(self, client):
        mouseKeys = pygame.mouse.get_pressed(3)
        if mouseKeys[0]:
            direction = getDirection(self)
            bullets.add(Bullet([self.rect.x,self.rect.y],direction,self))
            client.sendData({"type":"bullCreate","data":{"direction":direction,"spawnPoint":[self.rect.x+self.width,self.rect.y], "playerOrg":self.characterNo}})


    def gravity(self, cl, platform):
        if not self.collided:
            self.rect.y += 1
            if self.rect.y > 800 - self.height:
                self.rect.y = 800 - self.height
            else:
                #self.lastMoveMade = ["y", 1]
                moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "y", "movedTo": self.rect.y}}
                cl.sendData(moveMessage)
                self.lastPos = [self.rect.x, self.rect.y]


def sendPlatformInfo(platforms):
    data = []
    for platform in platforms.sprites():
        dictionary = {"platformNo": platform.platformNo,"platformTop":platform.rect.top, "platformLeft":platform.rect.left, "platformRight":platform.rect.right, "platformBottom":platform.rect.bottom}
        data.append(dictionary)
    return data

def publicGame(screen, clock, players, platforms, bullets, char):
    c = Client("127.0.0.1")
    c.connect()

    time.sleep(3)

    #print(players.sprites())

    clientPlayer = players.sprites()[0]
    c.setClientPlayer(clientPlayer)

    if clientPlayer.characterNo - 1 == 0:
        platformInfo = sendPlatformInfo(platforms)
        platformInfoDict = {"type": "platformInfo", "data": platformInfo}
        c.sendData(platformInfoDict)
    # print("Player added!")

    running = True

    # Run loop
    while running:

        clientPlayer.collided = False
        plat = None

        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                c.tellServerDisconn()
                exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseKey = pygame.mouse.get_pressed(3)

        collisions = pygame.sprite.groupcollide(platforms, players, False, False)
        for platform, player_list in collisions.items():
            for player in player_list:
                if player == clientPlayer:
                    clientPlayer.collided = True

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
        clock.tick(60)
        pygame.display.update()
    exit()

def privateCreate(screen, clock, players, platforms, bullets, char, creationData):
    server = Server(creationData["noOfPlayers"],creationData["lengthOfGame"], [[random.randint(0,800),random.randint(0,800)] for i in range(3)])
    server.start()

    c = Client(socket.gethostbyname(socket.gethostname()))
    c.connect()

    textOne = "Waiting for players to join!"
    textTwo = f"Join Code: {creationData['joinKey']}"

    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True

    c.enableWaiting()
    while c.checkWaiting():
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                c.waitingOver()
                exit()

        f.render_to(screen,(300,300), textOne, (0,0,0))
        f.render_to(screen, (300, 350), textTwo, (0, 0, 0))
        pygame.display.update()

    clientPlayer = players.sprites()[0]
    c.setClientPlayer(clientPlayer)

    running = True

    # Run loop
    while running:

        clientPlayer.collided = False
        plat = None

        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                c.tellServerDisconn()
                exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseKey = pygame.mouse.get_pressed(3)

        collisions = pygame.sprite.groupcollide(platforms, players, False, False)
        for platform, player_list in collisions.items():
            for player in player_list:
                if player == clientPlayer:
                    clientPlayer.collided = True

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
        clock.tick(60)
        pygame.display.update()
    exit()


def privateJoin(screen, clock, players, platforms, bullets, char, creationData):

    c = Client(creationData["data"]["IPAddress"])
    c.connect()

    textOne = "Waiting for players to join!"
    textTwo = f"Join Code: {creationData['joinKey']}"

    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True

    c.enableWaiting()
    while c.checkWaiting():
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                c.waitingOver()
                exit()

        f.render_to(screen, (300, 300), textOne, (0, 0, 0))
        f.render_to(screen, (300, 350), textTwo, (0, 0, 0))
        pygame.display.update()

    clientPlayer = players.sprites()[0]
    c.setClientPlayer(clientPlayer)

    running = True

    # Run loop
    while running:

        clientPlayer.collided = False
        plat = None

        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                c.tellServerDisconn()
                exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseKey = pygame.mouse.get_pressed(3)

        collisions = pygame.sprite.groupcollide(platforms, players, False, False)
        for platform, player_list in collisions.items():
            for player in player_list:
                if player == clientPlayer:
                    clientPlayer.collided = True

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

    # Only runs the code below if the player decides to join the public server (private server functionality needs to be worked on)
    beginInfo = gameStart(screen)

    if beginInfo["type"] == "publicGame":
        publicGame(screen, clock, players, platforms, bullets, char)

    if beginInfo["type"] == "privateCreate":
        privateCreate(screen, clock, players, platforms, bullets, char, beginInfo["data"])

    if beginInfo["type"] == "privateJoin":
        privateJoin(screen, clock, players, platforms, bullets, char, beginInfo["data"])