import pygame
import math

from time import time

'''
Name: Projectile
Purpose: Parent Class for all Projectiles
'''
class Projectile:
    '''
    Name: __init__
    Parameters: size: list[int], playerOrg: int, damage: int, spawnPoint: list[int]
    Returns: None
    Purpose: Constructor to set the initial values
    of the Projectile object
    '''
    def __init__(self, size: list[int], playerOrg: int, damage: int, spawnPoint: list[int], element: str) -> None:
        self._height: int = size[0]
        self._width: int = size[1]
        self._X: int = spawnPoint[0]
        self._Y: int = spawnPoint[1]
        self._playerOrigin: int = playerOrg
        self._damage: int = damage
        self._Element: str = element

    '''
    Name: getElement
    Parameters: None
    Returns: self._Element:str
    Purpose: Getter for the projectile's element
    '''
    def getElement(self) -> str:
        return self._Element

    '''
    Name: getDamage
    Parameters: None
    Returns: self._damage:int
    Purpose: Getter for the projectile's damage
    '''
    def getDamage(self) -> int:
        return self._damage

    '''
    Name: getPlayerOrigin
    Parameters: None
    Returns: self._playerOrigin:int
    Purpose: Getter for the playerID of the
    playerm who created this projectile    
    '''
    def getPlayerOrigin(self) -> int:
        return self._playerOrigin

    '''
    Name: getSize
    Parameters: None
    Returns: list[int]
    Purpose: Getter for the size of the projectile
    '''
    def getSize(self) -> list[int]:
        return [self._height, self._width]

    '''
    Name: getX
    Parameters: None
    Returns: self._X: int
    Purpose: Getter for the projectile's X coordinate
    '''
    def getX(self) -> int:
        return self._X

    '''
    Name: getY
    Parameters: None
    Returns: self._Y:int
    Purpose: Getter for the projectile's Y coordinate
    '''
    def getY(self) -> int:
        return self._Y

    '''
    Name: getHeight
    Parameters: None
    Returns: self._height:int
    Purpose: Getter for the height of the projectile
    '''
    def getHeight(self) -> int:
        return self._height

    '''
    Name: getWidth
    Parameters: None
    Returns: self._width:int
    Purpose: Getter for the width of the projectile
    '''
    def getWidth(self) -> int:
        return self._width


'''
Name: Bullet
Inherits: pygame.sprite.Sprite, Projectile
Purpose: Manages projectiles and projectile behaviour
'''
class Bullet(pygame.sprite.Sprite, Projectile):
    '''
    Name: __init__
    Parameters: spawnPoint:array, direction: array, player:int, size:list, damage:integer, element: str
    Returns: None
    Purpose: Constructor to set the initial values
    of the Bullet object
    '''
    def __init__(self,spawnPoint:list[int], direction:list[int], player:int, element:str, size:list[int]=[10,10],damage:int = 2):
        pygame.sprite.Sprite.__init__(self)
        Projectile.__init__(self,size, player, damage,spawnPoint, element)
        
        self.__direction = direction
        self.__gravity: int = lambda time: math.exp(time // 3)
        self.__updTimer: float = time()
        self.playerOrigin = player
        self.colour = (0,0,0)
        self.image = pygame.Surface([self.getWidth(),self.getHeight()])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image,self.colour,[self.getX(),self.getY(),self.getWidth(),self.getHeight()])
        self.rect = self.image.get_rect()
        self.rect.x = self._X
        self.rect.y = self._Y

    '''
    Name: update
    Parameters: None
    Returns: None
    Purpose: Update function that will update the object's rect position, depending on
    what the direction is
    '''
    def update(self):

        tempTime: float = time()

        if self.direction[0] is not None:
            self.rect.x -= self.direction[0]
        if self.direction[1] is not None:
            self.rect.y -= self.direction[1]

        if (int(self.__updTimer - tempTime)) % 1 == 0:
            self.__direction[1] -= self.__gravity(int(self.__updTimer-tempTime))


'''
Name: ConeAttack
Inherits: pygame.sprite.Sprite, Projectile
Purpose: Manages the cone attck projectile
'''
class ConeAttack(pygame.sprite.Sprite, Projectile):
    '''
    Name: __init__
    Parameters: spawnPoint: list[int], playerID: int, size: list[int], damage:int, element: str
    Returns: None
    Purpose: Constructor to set the initial values
    of the ConeAttack object
    '''
    def __init__(self, spawnPoint: list[int], playerID: int, element: str, size= [10,10], damage = 10) -> None:
        pygame.sprite.Sprite.__init__(self)
        Projectile.__init__(self,size, playerID, damage, spawnPoint, element)

        self.colour: tuple[int,int,int] = (200,200,200)
        self.image = pygame.image.load("spellCone.png")

        pygame.draw.rect(self.image, self.colour, [self.getX(), self.getY(), self.getWidth(), self.getHeight()])
        self.rect = self.image.get_rect()
        self.rect.x = self._X
        self.rect.y = self._Y
        self.__ticksExisted: int = 0

    '''
    Name: update
    Parameters: None
    Returns: None
    Purpose: Updates internal variables of the ConeAttack object 
    '''
    def update(self) -> None:
        self.__ticksExisted += 1
        if self.__ticksExisted > 120:
            pass


'''
Name: generateCooldown
Parameters: element
Returns: int
Purpose: Generates the cooldown time 
based on the element type
'''
def generateCooldown(element: str) -> int:
    if element == "Fire":
        return 3
    elif element == "Water":
        return 1
    elif element == "Earth":
        return 5
    else:
        raise ValueError("Internal Value Error. Element Passed in:",element)

