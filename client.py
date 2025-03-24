import socket, json, threading, pygame, sys
from time import sleep

class Client:
    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 50000
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
                        movedPlayer = players.sprites()[msg["data"]["clientNo"] - 1]
                        if msg["data"]["direction"] == "y":
                            movedPlayer.rect.y = msg["data"]["position"]
                        elif msg["data"]["direction"] == "x":
                            movedPlayer.rect.x = msg["data"]["position"]
                        players.sprites()[msg["data"]["clientNo"] - 1] = movedPlayer
                    if msg["type"] == "createPlat":
                        print("Created platform")
                        platforms.add(Platform([msg["data"]["positionX"], msg["data"]["positionY"]],[msg["data"]["sizeHeight"], msg["data"]["sizeWidth"]]))
                except json.JSONDecodeError as err:
                    print(data.decode())
                    print("JSON Syntax Error:", err)



def addCharacter(data):
    players.add(Character(data["positionList"],data["colourTuple"],data["clientNo"]))

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

    def move(self, cl,  platform, collided):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] == True:
            self.rect.y -= 4
            if self.rect.y < 0:
                self.rect.y = 0
            else:
                self.lastMoveMade = ["y",-4]
                moveMessage = {"type":"movement", "data":{"playerNo": self.characterNo, "direction":"y", "movedTo":self.rect.y}}
                cl.sendData(moveMessage)
        if keys[pygame.K_RIGHT] == True:
            self.rect.x += 2
            if self.rect.x > 800:
                self.rect.x = 800 - self.rect.x
            else:
                self.lastMoveMade = ["x", 2]
                moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x}}
                cl.sendData(moveMessage)
        if keys[pygame.K_LEFT] == True:
            self.rect.x -= 2
            if self.rect.x < 0:
                self.rect.x = 0
            else:
                self.lastMoveMade = ["x", -2]
                moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "x", "movedTo": self.rect.x}}
                cl.sendData(moveMessage)
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

    sleep(2)

    clientPlayer = players.sprites()[0]
    print("Player added!")


    running = True

    while running:

        collided = False
        plat = None

        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

        collisions = pygame.sprite.groupcollide(platforms, players, True, False)
        for platform, player_list in collisions.items():
            for player in player_list:
                platformPosition = [platform.X, platform.Y]
                platformSize = [platform.height, platform.width]
                collided = True
                platforms.add(Platform(platformPosition, platformSize))
                plat = platform

        clientPlayer.gravity(c, plat, collided)
        clientPlayer.move(c, plat, collided)
        platforms.draw(screen)
        players.draw(screen)
        clock.tick(60)
        pygame.display.update()

    sys.exit()
