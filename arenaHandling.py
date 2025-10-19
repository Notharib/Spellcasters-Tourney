import pygame

from random import randint

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
Name: onPlat
Parameters: player: object, platforms: object
Returns: boolean
Purpose: Determines whether a player is on top of a platform, and therefore
shouldn't be affected by gravity
'''
def onPlat(player, platforms):
    for platform in platforms.sprites():
        if (platform.rect.top == player.rect.bottom 
            or platform.rect.top == player.rect.bottom + 1 
            or platform.rect.top == player.rect.bottom - 1):
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
        dictionary = {
            "platformNo": platform.platformNo,
            "platformTop":platform.rect.top, 
            "platformLeft":platform.rect.left, 
            "platformRight":platform.rect.right, 
            "platformBottom":platform.rect.bottom}
        
        data.append(dictionary)
    
    return data

'''
Name: platformInfo
Parameters: platforms: pygame Sprite group, client:object, clientPlayer:object
Returns: None
Purpose: Send information about the platforms within the sprite group to the server
'''
def platformInfo(platforms, client, clientPlayer):
    if clientPlayer.getPlayerID() - 1 == 0:
        platformInfo = sendPlatformInfo(platforms)
        platformInfoDict = {"type": "platformInfo", "data": platformInfo}
        print(platformInfoDict)
        client.sendData(platformInfoDict)

'''
Name: platformGenerate
Parameters: amount: int, size: list[int], screenBounds: list[int],  playerSize: int
Returns: platforms: list[list[int]]
Purpose: Generates platform positions
'''
def platformGenerate(amount: int, size: list[int], screenBounds: list[int] = [800,800], playerSize: int = 40) -> list[list[int]]:
    platforms: list = []
    i: int = 0

    while i != amount:
        platform: list = [generateX(size[1], screenBounds[0]), generateY(size[0], screenBounds[1], playerSize)]
        platforms.append(platform)
        i += 1

    return platforms

'''
Name: generateX
Parameters: length: int, x_bound: int
Returns: int
Purpose: Generates a random X coordinate for the platforms
'''
def generateX(length: int, x_bound: int) -> int:
    lowerBound: int = int(x_bound * 0.025)
    upperBound: int = x_bound - length

    return randint(lowerBound, upperBound)

'''
Name: generateY
Parameters: width: int, y_bound: int, playerSize: int
Returns: int
Purpose: Generates a random Y coordinate for the platforms
'''
def generateY(width: int, y_bound: int, playerSize: int) -> int:
    lowerBound: int = playerSize + width + int(y_bound * 0.1)
    upperBound: int = y_bound - width - int(y_bound * 0.1)
    
    return randint(lowerBound, upperBound)