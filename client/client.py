import pygame, time, threading, socket, json, math
from menuScreens import gameStart, characterBuilder

class Client:
    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 50000
        self.clientNo = None
        self.__socket = None
        self.__noOfPlatforms = 0

    def connect(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__HOST, self.__PORT))
        threading.Thread(target=self.listen).start()

    def sendData(self,message):
        strMessage = json.dumps(message)
        self.__socket.send(strMessage.encode())

    def listen(self):
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

                    if msg["type"] == "MOVELEGAL":
                        #global clientPlayer
                        clientPlayer.legalMove()
                    if msg["type"] == "MOVENOTLEGAL":
                        #global clientPlayer
                        clientPlayer.illegalMove()

                except json.JSONDecodeError as err:
                    print(data.decode())
                    print("JSON Syntax Error:", err)

    def tellServerDisconn(self):
        msgDict = {"type":"disconn", "data":{"clientNo":self.clientNo}}
        self.sendData(msgDict)

def addCharacter(data):
    players.add(Character(data["positionList"],data["colourTuple"],data["clientNo"]))
    print("Player created!")

def createBullet(data):
    bullets.add(Bullet(data["spawnPoint"],data["direction"],data["playerOrg"]))

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


class Platform(pygame.sprite.Sprite):
    def __init__(self,position, size, platformNo):
        super().__init__()
        self.height = size[0]
        self.width = size[1]
        self.X = position[0]
        self.Y = position[1]
        self.colour = (0,255,0)
        self.platformNo = platformNo
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image,self.colour,[self.X,self.Y,self.width,self.height])
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y


class Bullet(pygame.sprite.Sprite):
    def __init__(self,spawnPoint, direction, player, size=[10,10],damage = 2):
        super().__init__()
        self.height = size[0]
        self.width = size[1]
        self.X = spawnPoint[0]
        self.Y = spawnPoint[1]
        self.direction = direction
        self.playerOrigin = player
        self.colour = (0,0,0)
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image,self.colour,[self.X,self.Y,self.width,self.height])
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y
        self.damage = damage

    def update(self):
        if self.direction[0] is not None:
            self.rect.x -= self.direction[0]
        if self.direction[1] is not None:
            self.rect.y -= self.direction[1]

        if self.rect.y > 800 or self.rect.y < 0 or self.rect.x > 800 or self.rect.x < 0:
            bullets.remove(self)

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

    def youDied(self):
        if self.HP == 0:
            running = True
            text = """You Died! 
                Press ENTER to respawn!"""
            f = pygame.font.SysFont("Comic Sans MS",24)
            output = f.render(text,True,(0,0,0))
            while running:
                screen.fill((255,255,255))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_RETURN]:
                            self.health = 10
                            running = False
                screen.blit(output,(200,400))
                pygame.display.update()

    def legalMove(self):
        self.lastLegalPos = self.lastPos

    def onPlat(self):
        for platform in platforms.sprites():
            if platform.rect.top == self.rect.bottom or platform.rect.top == self.rect.bottom + 1 or platform.rect.top == self.rect.bottom - 1:
                print("on platform")
                return True
        return False

    def illegalMove(self):
        global collided
        if (not self.onPlat()) and collided:
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

    def move(self, cl, platform, collided):
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
                        moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "y", "movedTo": self.rect.y, "collided":collided}}
                        cl.sendData(moveMessage)
                        time.sleep(0.01)
                        moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x, "collided":collided}}
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
                        moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "y", "movedTo": self.rect.y, "collided":collided}}
                        cl.sendData(moveMessage)
                        time.sleep(0.01)
                        moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x, "collided":collided}}
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
                    moveMessage = {"type":"movement", "data":{"playerNo": self.characterNo, "direction":"y", "movedTo":self.rect.y, "collided":collided}}
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
                    moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x, "collided":collided}}
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
                    moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x, "collided":collided}}
                    cl.sendData(moveMessage)
                    self.lastPos = [self.rect.x, self.rect.y]
                    time.sleep(0.01)

    def fire(self, client):
        mouseKeys = pygame.mouse.get_pressed(3)
        if mouseKeys[0]:
            direction = self.getDirection()
            bullets.add(Bullet([self.rect.x,self.rect.y],direction,self))
            client.sendData({"type":"bullCreate","data":{"direction":direction,"spawnPoint":[self.rect.x+self.width,self.rect.y], "playerOrg":self}})

    def getDirection(self):
        mousePos = pygame.mouse.get_pos()
        MPVector = [self.rect.x - mousePos[0], self.rect.y - mousePos[1]]
        print(MPVector)
        hyppotenuse = math.sqrt((MPVector[0]**2)+(MPVector[1]**2))
        divider = hyppotenuse // 10
        for i in range(2):
            MPVector[i] //= divider

        print(MPVector)
        return MPVector


    def gravity(self, cl, platform, collided):
        if not collided:
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
    begin = gameStart(screen)

    if begin:
        c = Client()
        c.connect()

        time.sleep(3)

        clientPlayer = players.sprites()[0]

        if clientPlayer.characterNo - 1 == 0:
            platformInfo = sendPlatformInfo(platforms)
            platformInfoDict = {"type":"platformInfo","data":platformInfo}
            c.sendData(platformInfoDict)
        #print("Player added!")


        running = True

        while running:

            collided = False
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
                        collided = True

            pHit = pygame.sprite.groupcollide(bullets, players, False, False)
            for b, p_list in pHit.items():
                for pl in p_list:
                    if pl != b.playerOrigin:
                        pl.HP -= b.damage
                        pl.youDied()
                        bullets.remove(b)

            bullets.update()
            clientPlayer.gravity(c, plat, collided)
            clientPlayer.move(c, plat, collided)
            clientPlayer.fire(c)
            platforms.draw(screen)
            bullets.draw(screen)
            players.draw(screen)
            clock.tick(60)
            pygame.display.update()
        exit()
    exit()
