from random import (randint, choice)


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
Purpose: Client class for the private server, to make managing data about 
any given player easier
'''
class Client:
    '''
    Name: __init__
    Parameters: conn:object, spawnPoint:tuple[int,int] playerID:integer, size:list
    Returns: None
    Purpose: Constructor to set the initial values
    of the Client object
    '''
    def __init__(self, conn, spawnPoint:list[int], playerID:int, size: list[int] =[40,40]) -> None:
        self.__client = conn
        self.__spawnPoint: tuple[int,int] = spawnPoint
        self.__element: str|None = None
        self.__spellCaster: str|None = None
        self.__playerID: int = playerID
        self.__colour: tuple[int,int,int] = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.position: list[int]  = list(spawnPoint)
        self.__size: list[int] = size

    '''
    Name: sendData
    Parameters: msgToSend:dictionary
    Returns: None
    Purpose: Sends data through the connection
    '''
    def sendData(self, msgToSend:dict) -> None:
        self.__client.send(msgToSend)

    # Getters and setters

    '''
    Name: setElement
    Parameters: element: str
    Returns: None
    Purpose: Setter for self.__element
    '''
    def setElement(self, element:str) -> None:
        self.__element = element

    '''
    Name: setCaster
    Parameters: spellCaster: str
    Returns: None
    Purpose: Setter for self.__spellCaster
    '''
    def setCaster(self, spellCaster:str) -> None:
        self.__spellCaster = spellCaster

    '''
    Name: getSpawnPoint
    Parameters: None
    Returns: self.__spawnPoint:list
    Purpose: Getter for self.__spawnPoint
    '''
    def getSpawnPoint(self) -> list:
        return self.__spawnPoint

    '''
    Name: getSize
    Parameters: None
    Returns: self.__size:list
    Purpose: Getter for self.__size 
    '''
    def getSize(self) -> list:
        return self.__size

    '''
    Name: getClient
    Parameters: None
    Returns: self.__client:object
    Purpose: Getter for self.__client
    '''
    def getClient(self):
        return self.__client

    '''
    Name: getPlayerID
    Parameters: None
    Returns: self.__playerID:integer
    Purpose: Getter for self.__playerID
    '''
    def getPlayerID(self) -> int:
        return self.__playerID

    '''
    Name: getElement
    Parameters: None
    Returns: self.__element:str
    Purpose: Getter for self.__element
    '''
    def getElement(self) -> str:
        return self.__element

    '''
    Name: getPlayerColour
    Parameters: None
    Returns: self.__colour:tuple
    Purpose: Getter for self.__colour
    '''
    def getPlayerColour(self) -> tuple[int,int,int]:
        return self.__colour

    '''
    Name: getCaster
    Parameters: None
    Returns: self.__spellCaster:str
    Purpose: Getter for self.__spellCaster
    '''
    def getCaster(self) -> str:
        return self.__spellCaster

