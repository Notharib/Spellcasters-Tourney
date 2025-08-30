from random import randint, choice

from characterCreation import BaseCharacter

'''
Name: generatePlatforms
Parameters: platform: list[int], size:list[int]
Returns: retVal:list
Purpose: Generates the platforms for the server to use
'''
def generatePlatforms(platPositions: list[list[int]], size: list[int] = [20,500]) -> list:
    retVal: list = []
    for platform in platPositions:
        tempPlat = Platform(platform,size)
        coords: dict = generatePlatCoords(platform, size)
        tempPlat.setLeft(coords["left"])
        tempPlat.setRight(coords["right"])
        tempPlat.setTop(coords["top"])
        tempPlat.setBottom(coords["bottom"])
        retVal.append(tempPlat)
    return retVal
'''
Name: generatePlatCoords
Parameters: platform: list[int], size:list[int]
Returns: dict
Purpose: Generates the position of the left, right, top, and
bottom coordinate, based on its size and top left coords
'''
def generatePlatCoords(platform: list[int], size: list[int]) -> dict:
    return {"left": platform[0], "right": platform[0] + size[1], "top": platform[1], "bottom": platform[1] + size[0]}

'''
Name: Platform
Purpose: To have platforms that players are able to move around on
'''
class Platform:
    '''
    Name: __init__
    Parameters: position: list, size:list
    Returns: None
    Purpose: Constructor to set the initial values
    of the platform object
    '''
    def __init__(self, position, size=[20,500]):
        self.__position = position
        self.__size = size
        self.__colour = (0,0,255)
        self.__top = None
        self.__left = None
        self.__right = None
        self.__bottom = None
    # Getters and Setters

    '''
    Name: getPos
    Parameters: None
    Returns: self.__position:list
    Purpose: Getter for self.__position
    '''
    def getPos(self):
        return self.__position

    '''
    Name: getPos
    Parameters: None
    Returns: self.__size:list
    Purpose: Getter for self.__size
    '''
    def getSize(self):
        return self.__size

    '''
    Name: getTop
    Parameters: None
    Returns: self.__top
    Purpose: Getter for self.__top
    '''
    def getTop(self):
        return self.__top

    '''
    Name: getBottom
    Parameters: None
    Returns: self.__bottom
    Purpose: Getter for self.__bottom
    '''
    def getBottom(self):
        return self.__bottom

    '''
    Name: getLeft
    Parameters: None
    Returns: self.__left
    Purpose: Getter for self.__left
    '''
    def getLeft(self):
        return self.__left

    '''
    Name: getRight
    Parameters: None
    Returns: self.__right
    Purpose: Getter for self.__right
    '''
    def getRight(self):
        return self.__right

    '''
    Name: setTop
    Parameters: top
    Returns: None
    Purpose: Setter for self.__top
    '''
    def setTop(self, top):
        self.__top = top
        return None

    '''
    Name: setLeft
    Parameters: left
    Returns: None
    Purpose: Setter for self.__left
    '''
    def setLeft(self, left):
        self.__left = left
        return None

    '''
    Name: setRight
    Parameters: right
    Returns: None
    Purpose: Setter for self.__right
    '''
    def setRight(self, right):
        self.__right = right
        return None

    ''' 
    Name: setBottom
    Parameters: bottom
    Returns: None
    Purpose: Setter for self.__bottom
    '''
    def setBottom(self, bottom):
        self.__bottom = bottom
        return None

    '''
    Name: __repr__
    Parameters: None
    Returns: self.__postion
    Purpose: Defines how this object should be represented if printed directly
    '''
    def __repr__(self):
        return self.__position

'''
Name: Client
Purpose: Client Class to handle how the Private Server should deal with
players/connections
'''
class Client(BaseCharacter):
    '''
    Name: __init__
    Parameters: conn:object, position:list[int], playerNo:int
    Returns: None
    Purpose: Constructor to set the initial values
    of the Client object
    '''
    def __init__(self, conn, position: list[int], playerNo: int) -> None:
        super().__init__()
        self.__conn = conn
        self.__X: int = position[0]
        self.__Y: int = position[1]
        self.__playerID: int = playerNo

    '''
    Name: getClient
    Parameters: None
    Returns: self.__conn
    Purpose: Getter for the client's connection
    '''
    def getClient(self) -> any:
        return self.__conn

    '''
    Name: getX
    Parameters: None
    Returns: self.__X:int
    Purpose: Getter for the client's X
    coordinate
    '''
    def getX(self) -> int:
        return self.__X
    
    '''
    Name: getY
    Parameters: None
    Returns: self.__Y: int
    Purpose: Getter for the client's Y
    coordinate
    '''
    def getY(self) -> int:
        return self.__Y

    '''
    Name: getPlayerID
    Parameters: None
    Returns: self.__playerID:int
    Purpose: Getter for the client's
    playerID
    '''
    def getPlayerID(self) -> int:
        return self.__playerID

    '''
    Name: getSpawnPoint
    Parameters: None
    Returns: list[int]
    Purpose: Getter for the client's
    initial position
    '''
    def getSpawnPoint(self) -> list[int]:
        return [self.__X, self.__Y]

    '''
    Name: getPlayerColour
    Parameters: None
    Returns: self.__colour:tuple[int,int,int]
    Purpose: Getter for the client's
    colour
    '''
    def getPlayerColour(self) -> tuple[int,int,int]:
        return self.__colour

    '''
    Name: getCaster
    Parameters: None
    Returns: self.__Caster:str
    Purpose: Getter for the client's
    caster
    '''
    def getCaster(self) -> str:
        return self._Caster

    '''
    Name: getElement
    Parameters: None
    Returns: self._Element:str
    Purpose: Getter for the client's
    element
    '''
    def getElement(self) -> str:
        return self._Element

    '''
    Name: setPosition
    Parameters: position:list[int]
    Returns: None
    Purpose: Setter for the client's position
    '''
    def setPosition(self, position:list[int]) -> None:
        self.__X = position[0]
        self.__Y = position[1]

    '''
    Name: setHP
    Parameters: HP:int
    Returns: None
    Purpose: Setter for the client's HP
    '''
    def setHP(self, HP:int) -> None:
        self._HP = HP

    '''
    Name: setElement
    Parameters: element:str
    Returns: None
    Purpose: Setter for the client's Element
    '''
    def setElement(self, element:str) -> None:
        self._Element = element

    '''
    Name: setHP
    Parameters: caster:str
    Returns: None
    Purpose: Setter for the client's Caster
    '''
    def setCaster(self, caster: str) -> None:
        self._Caster = caster
