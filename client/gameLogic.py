import pygame, math

# Element Classes

class Fire:
    def __init__(self):
        self.__opposite = "Water"
        self.__type = "Fire"

    def __repr__(self):
        return self.__type

class Water:
    def __init__(self):
        self.__opposite = "Fire"
        self.__type = "Water"

    def __repr__(self):
        return self.__type

# Spellcaster Classes

class Wizard:
    def __init__(self):
        self.__type = "Wizard"

class Druid:
    def __init__(self):
        self.__type = "Druid"

# Non-player objects to be used within the game

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

# Objects mainly only used within menus

class TextBox(pygame.sprite.Sprite):
    def __init__(self, position, text, allow="allInput",  typing=False):
        super().__init__()
        self.X = position[0]
        self.Y = position[1]
        self.height = 30
        self.width = 50
        self.colour = (200,200,200)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image, self.colour, (self.X, self.Y, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y
        self.typing = typing
        self.text = text
        self.allow = allow

    def checkIfExample(self):
        if self.text == "EXAMPLE":
            return True
        else:
            return False

    def update(self, keys):
        if self.typing:
            if self.allow == "allInput" or self.allow == "numberInput":
                if keys[pygame.K_BACKSPACE]:
                    if self.checkIfExample():
                        self.text = ""
                    else:
                        pass
                elif keys[pygame.K_1]:
                    if not self.checkIfExample():
                        self.text += "1"
                    else:
                        self.text = "1"



# Used so that the user can select which text box they are actually typing into
class Pointer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.X = pygame.mouse.get_pos()[0]
        self.Y = pygame.mouse.get_pos()[1]
        self.height = 1
        self.width = 1
        self.colour =  (255,255,255)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image, self.colour, (self.X, self.Y, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y

    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.rect.x = mousePos[0]
        self.rect.y = mousePos[1]

# General functions

def getDirection(player):
    mousePos = pygame.mouse.get_pos()
    MPVector = [player.rect.x - mousePos[0], player.rect.y - mousePos[1]]
    print(MPVector)
    hyppotenuse = math.sqrt((MPVector[0] ** 2) + (MPVector[1] ** 2))
    divider = hyppotenuse // 10
    for i in range(2):
        MPVector[i] //= divider

    print(MPVector)
    return MPVector

def youDied(player, screen):
    if player.HP == 0:
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
                        player.health = 10
                        running = False
            screen.blit(output,(200,400))
            pygame.display.update()
    return player

def onPlat(player, platforms):
    for platform in platforms.sprites():
        if platform.rect.top == player.rect.bottom or platform.rect.top == player.rect.bottom + 1 or platform.rect.top == player.rect.bottom - 1:
            print("on platform")
            return True
    return False

if __name__ == "__main__":
    pass