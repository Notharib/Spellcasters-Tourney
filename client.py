import socket, json, threading, pygame, sys
import time


class Client:
    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 50001
        self.clientNo = None
        self.__socket = None

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
                        platforms.add(Platform([msg["data"]["positionX"], msg["data"]["positionY"]],[msg["data"]["sizeHeight"], msg["data"]["sizeWidth"]]))
                    if msg["type"] == "disconn":
                        players.remove(players.sprites()[msg["data"]["clientNo"]])
                        print("Player Disconnected")

                except json.JSONDecodeError as err:
                    print(data.decode())
                    print("JSON Syntax Error:", err)

    def tellServerDisconn(self):
        msgDict = {"type":"disconn", "data":{"clientNo":self.clientNo}}
        self.sendData(msgDict)


def addCharacter(data):
    players.add(Character(data["positionList"],data["colourTuple"],data["clientNo"]))
    print("Player created!")

class Platform(pygame.sprite.Sprite):
    def __init__(self,position, size):
        super().__init__()
        self.height = size[0]
        self.width = size[1]
        self.X = position[0]
        self.Y = position[1]
        self.colour = (0,255,0)
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image,self.colour,[self.X,self.Y,self.width,self.height])
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y


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
        self.lastMoveMade = []
        self.lastNonColPos =[]

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


    def checkIfLegal(self,direction, amount):
        return True
        # if direction == "y":
        #     for platform in platforms.sprites():
        #         if (self.rect.y - amount) - 40 == platform.rect.bottom:
        #             print("Top bounce")
        #             return False
        #         else:
        #             return True
        # else:
        #     if amount * 1 <= -1:
        #         remover = 40
        #     else:
        #         remover = -40
        #     for platform in platforms.sprites():
        #         if (self.rect.x - amount) - remover == platform.rect.left:
        #             print("Left bounce")
        #             return False
        #         elif (self.rect.x - amount) - remover == platform.rect.right:
        #             print("Right bounce")
        #             return False
        #         else:
        #             return True


    def move(self, cl,  platform, collided):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] == True and keys[pygame.K_LEFT] == True:
            legalMove = self.checkIfLegal("y",4)
            if legalMove:
                self.rect.y -= 4
                legalMove = self.checkIfLegal("x",2)
                if legalMove:
                    self.rect.x -= 2
                    if self.rect.y < 0:
                        self.rect.y = 0
                    elif self.rect.x < 0:
                        self.rect.x = 0
                    else:
                        self.lastMoveMade = ["y", -4]
                        moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "y", "movedTo": self.rect.y}}
                        cl.sendData(moveMessage)
                        time.sleep(0.01)
                        moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x}}
                        cl.sendData(moveMessage)
        elif keys[pygame.K_UP] == True and keys[pygame.K_RIGHT] == True:
            legalMove = self.checkIfLegal("y", 4)
            if legalMove:
                self.rect.y -= 4
                legalMove = self.checkIfLegal("x", -2)
                if legalMove:
                    self.rect.x += 2
                    if self.rect.y < 0:
                        self.rect.y = 0
                    elif self.rect.x > 800:
                        self.rect.x = 800 - self.rect.x
                    else:
                        self.lastMoveMade = ["y", -4]
                        moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "y", "movedTo": self.rect.y}}
                        cl.sendData(moveMessage)
                        time.sleep(0.01)
                        moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x}}
                        cl.sendData(moveMessage)

        elif keys[pygame.K_UP] == True:
            legalMove = self.checkIfLegal("y", 4)
            if legalMove:
                self.rect.y -= 4
                if self.rect.y < 0:
                    self.rect.y = 0
                else:
                    self.lastMoveMade = ["y",-4]
                    moveMessage = {"type":"movement", "data":{"playerNo": self.characterNo, "direction":"y", "movedTo":self.rect.y}}
                    cl.sendData(moveMessage)
                    time.sleep(0.01)
        elif keys[pygame.K_RIGHT] == True:
            legalMove = self.checkIfLegal("x", -2)
            if legalMove:
                self.rect.x += 2
                if self.rect.x > 800:
                    self.rect.x = 800 - self.rect.x
                else:
                    self.lastMoveMade = ["x", 2]
                    moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x}}
                    cl.sendData(moveMessage)
                    time.sleep(0.01)
        elif keys[pygame.K_LEFT] == True:
            legalMove = self.checkIfLegal("x", 2)
            if legalMove:
                self.rect.x -= 2
                if self.rect.x < 0:
                    self.rect.x = 0
                else:
                    self.lastMoveMade = ["x", -2]
                    moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x}}
                    cl.sendData(moveMessage)
                    time.sleep(0.01)
        if collided:
            score = False
            if platform.rect.bottom == self.rect.top:
                self.rect.y = self.lastNonColPos[1]
            if platform.rect.right == self.rect.left:
                self.rect.x = self.lastNonColPos[0]
            if platform.rect.left == self.rect.right:
                self.rect.x = self.lastNonColPos[0]
            if not score:
                self.lastNonColPos = [self.rect.x, self.rect.y]
        else:
            self.lastNonColPos = [self.rect.x,self.rect.y]


    def gravity(self, cl, platform, collided):
        if not collided:
            if self.lastMoveMade != ["y",2]:
                self.rect.y += 1
                if self.rect.y > 800 - self.height:
                    self.rect.y = 800 - self.height
                else:
                    #self.lastMoveMade = ["y", 1]
                    moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "y", "movedTo": self.rect.y}}
                    cl.sendData(moveMessage)
        if collided:
            if platform.rect.top == self.rect.bottom:
                self.rect.y -= 1



if __name__ == '__main__':
    pygame.display.init()
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

    c = Client()
    c.connect()

    time.sleep(3)

    clientPlayer = players.sprites()[0]
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

        collisions = pygame.sprite.groupcollide(platforms, players, False, False)
        for platform, player_list in collisions.items():
            for player in player_list:
                collided = True


        clientPlayer.gravity(c, plat, collided)
        clientPlayer.move(c, plat, collided)
        platforms.draw(screen)
        players.draw(screen)
        clock.tick(60)
        # print("event loop ran")
        pygame.display.update()
