import pygame

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
    def __init__(self, size: list[int], playerOrg: int, damage: int, spawnPoint: list[int]) -> None:
        self._height: int = size[0]
        self._width: int = size[1]
        self._X: int = spawnPoint[0]
        self._Y: int = spawnPoint[1]
        self._playerOrigin: int = playerOrg
        self._damage: int = damage

    def getDamage(self) -> int:
        return self._damage

    def getPlayerOrigin(self) -> int:
        return self._playerOrigin

    def getSize(self) -> list[int]:
        return [self._height, self._width]


'''
Name: Bullet
Inherits: pygame.sprite.Sprite, Projectile
Purpose: Manages projectiles and projectile behaviour
'''
class Bullet(pygame.sprite.Sprite, Projectile):
    '''
    Name: __init__
    Parameters: spawnPoint:array, direction: array, player:int, size:list, damage:integer
    Returns: None
    Purpose: Constructor to set the initial values
    of the Bullet object
    '''
    def __init__(self,spawnPoint, direction, player, size=[10,10],damage = 2):
        
        pygame.sprite.Sprite.__init__()
        Projectile.__init__(size, player, damage,spawnPoint)
        
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


class ConeAttack(pygame.sprite.Sprite, Projectile):

    def __init__(self, spawnPoint, playerNo, size= [10,10], damage = 10):
        pygame.sprite.Sprite.__init__()
        Projectile.__init__(size, playerNo, damage, spawnPoint)

        self._colour: tuple[int,int,int] = (200,200,200)
        self._image = pygame.Surface(size)
        self._image.fill(self._colour)
        self.__RECT = pygame.Rect((spawnPoint[0], spawnPoint[1]), (size[0]+10, size[1]+10))

        pygame.draw.arc(self._image, self._colour, [1,2], width=2)
        self._rect = self._image.get_rect()
        self._rect.x = self._X
        self._rect.y = self._y
