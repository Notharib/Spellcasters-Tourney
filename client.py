import socket, json, threading, pygame
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
                msg = dict(json.loads(data.decode()))
                if msg["type"] == "clientNo":
                    self.clientNo = msg["data"]["clientNo"]
                    addCharacter(msg["data"])
                if msg["type"] == "playerJoin":
                    addCharacter(msg["data"])
                if msg["type"] == "movement":
                    pass


def addCharacter(data):
    players.add(Character(data["position"],data["colour"],data["clientNo"]))


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

    def move(self, cl):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] == True:
            self.rect.y -= 1
            if self.rect.y < 0:
                self.rect.y = 0
        moveMessage = {"type":"movement", "data":{"playerNo": self.characterNo, "direction":"y", "movedTo":self.rect.y}}
        cl.sendData(moveMessage)
        if keys[pygame.K_DOWN] == True :
            self.rect.y += 1
            if self.rect.y > 800 - self.height:
                self.rect.y = 800 - self.height
            moveMessage = {"type": "movement","data": {"playerNo": self.characterNo, "direction": "y", "movedTo": self.rect.y}}
            cl.sendData(moveMessage)
        if keys[pygame.K_RIGHT] == True:
            self.rect.x += 1
            if self.rect.x > 800:
                self.rect.x = 800 - self.rect.x
        if keys[pygame.K_LEFT] == True:
            self.rect.x -= 1
            if self.rect.x < 0:
                self.rect.x = 0


if __name__ == '__main__':
    pygame.display.init()
    WINDOW_SIZE = (800, 800)

    RED = (250, 9, 1)
    GREEN = (2, 249, 0)
    BLUE = (0, 0, 240)
    PURPLE = (160, 32, 240)

    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    players = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    c = Client()
    c.connect()

    sleep(2)

    clientPlayer = players.sprites()[0]
    print("Player added!")

    platforms.add(Platform([199,199], [20,200]))

    running = True

    while running:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
        clientPlayer.move()
        
        collisions = pygame.sprite.groupcollide(players, platforms,True,False)
        for play,plat_list in collisions.items():
            for platform in plat_list:
                X = platform.X
                Y = platform.Y
                position = [X,Y]
                height = platform.height
                width = platform.width
                size = [height,width]
                
