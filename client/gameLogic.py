import pygame, math, requests, json

# Non-player objects to be used within the game

'''
Name: Platform
Inherits: pygame.sprite.Sprite
Purpose: To have platforms that players are able to move around on
'''
class Platform(pygame.sprite.Sprite):
    '''
    Name: __init__
    Parameters: position:list, size: list, platformNo: integer
    Returns: None
    Purpose: Constructor to set the initial values
    of the Platform object
    '''
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

'''
Name: Bullet
Inherits: pygame.sprite.Sprite
Purpose: Manages projectiles and projectile behaviour
'''
class Bullet(pygame.sprite.Sprite):
    '''
    Name: __init__
    Parameters: spawnPoint:array, direction: array, player:object, size:list, damage:integer
    Returns: None
    Purpose: Constructor to set the initial values
    of the Bullet object
    '''
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

    '''
    Name: update
    Parameters: None
    Returns: None
    Purpose: Update function that will update the object's rect position, depending on
    what the direction is
    '''
    def update(self):
        if self.direction[0] is not None:
            self.rect.x -= self.direction[0]
        if self.direction[1] is not None:
            self.rect.y -= self.direction[1]


# General functions

'''
Name: getLeaderboard
Parameters: serverType:string, playerNo:integer, serverKey:None, client=None
Returns: leaderboard:dictionary
Purpose: Gets the current updated version of the leaderboard for the player to see
'''
def getLeaderboard(serverType, playerNo, serverKey=None, client=None):
    if serverType == "public":
        if client is None:
            raise Exception("Client object is required for public server leaderboards")
        else:
            pass
    elif serverType == "private":
        if serverKey is None:
            raise Exception("Server key is required for private server leaderboards")
        else:
            jsonInfo = {
                "serverKey":serverKey,
                "playerNo":playerNo
            }
            leaderboard = requests.get("http://127.0.0.1:5000/privateLeaderCheck", json={jsonInfo}).json()
            return leaderboard
    else:
        raise ValueError("Server type must be either public or private")


'''
Name: getDirection
Parameters: player:object
Returns: MPVector:list
Purpose: Gets the direction vector that the projectile needs to move in
'''
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

'''
Name: youDied
Parameters: player:object, screen:object
Returns: player: object
Purpose: Event loop to handle what happens when a player runs out of health
'''
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

'''
Name: onPlat
Parameters: player: object, platforms: object
Returns: boolean
Purpose: Determines whether a player is on top of a platform, and therefore
shouldn't be affected by gravity
'''
def onPlat(player, platforms):
    for platform in platforms.sprites():
        if platform.rect.top == player.rect.bottom or platform.rect.top == player.rect.bottom + 1 or platform.rect.top == player.rect.bottom - 1:
            print("on platform")
            return True
    return False

'''
Name: sendPlatformInfo
Parameters: platforms: pygame Sprite Group
Returns: data:list
Purpose: Creates a list of all the information about all the platforms
'''
def sendPlatformInfo(platforms):
    data = []
    for platform in platforms.sprites():
        dictionary = {"platformNo": platform.platformNo,"platformTop":platform.rect.top, "platformLeft":platform.rect.left, "platformRight":platform.rect.right, "platformBottom":platform.rect.bottom}
        data.append(dictionary)
    return data

'''
Name: platformInfo
Parameters: platforms: pygame Sprite group, client:object, clientPlayer:object
Returns: None
Purpose: Send information about the platforms within the sprite group to the server
'''
def platformInfo(platforms, client, clientPlayer):
    if clientPlayer.characterNo - 1 == 0:
        platformInfo = sendPlatformInfo(platforms)
        platformInfoDict = {"type": "platformInfo", "data": platformInfo}
        print(platformInfoDict)
        client.sendData(platformInfoDict)

if __name__ == "__main__":
    pass