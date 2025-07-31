import math
import random

import pygame
import requests

# Non-player objects to be used within the game

class queue:
    '''
    Name: queue
    Purpose: To handle the functions of a queue data type
    '''
    def __init__(self) -> None:
        '''
        Name: __init__
        Parameters: self
        Returns: None
        Description: Initialises the Queue as a list with 10 Null elements and
        initialises the rear to -1
        '''
        self.__data: list = [None for i in range(20)]
        self.__back: int = -1

    def dumpData(self) -> None:
        '''
        Name: dumpData
        Parameters: self
        Returns: None
        Description: Used in unit tests to dump any leftover data from a previous test
        '''
        self.__data = [None for i in range(20)]
        self.__back = -1

    def loadData(self) -> None:
        '''
        Name: loadData
        Parameters: self
        Returns: None
        Description: Used in the unit tests just to generate random data to be used
        '''
        self.__data = [random.randint(0,100) for i in range(10)]
        self.__back = 9

    def getFront(self):
        '''
        Name: getFront
        Parameters: self
        Returns: None
        Description: Returns the front element of the queue
        '''
        return self.__data[0]

    def getBack(self):
        '''
        Name: getBack
        Parameters: self
        Returns: self._data[self.__back]
        Description: Checks if the Queue is full, if not adds new element
        to the rear of the Queue and updates the rear pointer
        '''
        if not self.is_empty():
            return self.__data[self.__back]
        else:
            raise Exception("Attempted to get back of an empty queue")

    def enqueue(self, data) -> None:
        '''
        Name: enqueue
        Parameters: self, data
        Returns: None
        Description: Checks if the Queue is full, if not adds new element
        to the rear of the Queue and updates the rear pointer
        '''
        if not self.is_full():
            if self.__back == -1:
                self.__data[0] = data
                self.__back = 0
            else:
                self.__back += 1
                self.__data[self.__back] = data
        else:
            raise Exception("Attempted to enter data into a queue that is full")

    def dequeue(self):
        '''
        Name: dequeue
        Parameters: self
        Returns: String|Integer|Dictionary
        Description: Returns the item at
        the front of the Queue and updates the front pointer
        '''
        if not self.is_empty():
            org = self.__data[0]

            self.__data.pop(0)
            self.__data.append(None)

            noneValues = 0
            for item in self.__data:
                if item is None:
                    noneValues += 1
            if noneValues == 20:
                self.__back = -1

            return org
        else:
            raise Exception("Attempted to dequeue an empty queue")

    def is_full(self) -> bool:
        '''
        Name: isfull
        Parameters: Self
        Returns: Boolean
        Description: Returns True if the Queue is full and False if not
        '''
        return self.__back == 19

    def is_empty(self) -> bool:
        '''
        Name: is_empty
        Parameters: Self
        Returns: Boolean
        Description: Returns True if the Queue is empty and False if not
        '''
        return self.__back == -1

    def spaces_free(self) -> int:
        '''
        Name: spaces_free
        Parameters: Self
        Returns: Integer
        Description: Returns how many empty spaces remain in the Queue
        '''
        noneValues: int = 0
        for item in self.__data:
            if item is None:
                noneValues += 1

        return noneValues

'''
Name: Leaderboard
Inherits: pygame.sprite.Sprite
Purpose: To display what the current leaderboard is
'''
class Leaderboard(pygame.sprite.Sprite):
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Leaderboard object
    '''
    def __init__(self):
        super().__init__()
        self.__leaderboard: dict = {}
        self.__displayText: str = ""
        self.X: int = 200
        self.Y: int = 0
        self.width: int = 400
        self.height: int = 300
        self.colour: tuple = (0,0,255)
        self.image: pygame.Surface = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image, self.colour, [self.X, self.Y, self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x: int = self.X
        self.rect.y: int = self.Y

    '''
    Name: update
    Parameters: leaderboard:dictionary
    Returns: None
    Purpose: Updates the values of different variables within the class as needed
    '''
    def update(self, leaderboard: dict):
        self.__displayText = ""
        self.__leaderboard = leaderboard
        leaderList: list[list[str]] = self.setupLeaderStructure()
        for i in range(len(leaderList)):
            if i == 0:
                self.__displayText += "1: {firstUser}, {firstDeaths}".format(firstUser=leaderList[i][0], firstDeaths=leaderList[i][1])
            else:
                self.__displayText += "\n{position}: {user}, {deathCount}".format(position=i+1, user=leaderList[i][0], deathCount=leaderList[i][1])
        print(self.__displayText)

    '''
    Name: getDisplayText
    Parameters: None
    Returns: string
    Purpose: Getter for the displayText variable
    '''
    def getDisplayText(self) -> str:
        return self.__displayText

    '''
    Name: getLeaderboard 
    Parameters: None 
    Returns: dictionary 
    Purpose: Getter for the leaderboard variable
    '''    
    def getLeaderboard(self) -> dict:
        return self.__leaderboard


    '''
    Name: addToLeader
    Parameters: examplePlayer:list
    Returns: None
    Purpose: Function only used for unit testing to add players to
    the leaderboard
    '''
    def addToLeader(self,examplePlayer) -> None:
        self.__leaderboard[examplePlayer[0]] = examplePlayer[1]

    '''
    Name: setupLeaderStructure
    Parameters: None
    Returns: orderedLeader:list
    Purpose: Organises the leaderboard so that
    '''
    def setupLeaderStructure(self):
        keysToPop = []
        for key in list(self.__leaderboard.keys()):
            if self.__leaderboard[key] is None:
                keysToPop.append(key)
        if len(keysToPop) != 0:
            for key in keysToPop:
                self.__leaderboard.pop(key)

        deathValues = list(self.__leaderboard.values())
        # print(deathValues)

        orderedDeath = merge_sort(deathValues)
       # deathValues.sort()
       # orderedDeath = deathValues

        orderedLeader = []
        for deathValue in orderedDeath:
            for key in self.__leaderboard.keys():
                if self.__leaderboard[key] == deathValue:
                    orderedLeader.append([key, deathValue])
                    break
        return orderedLeader

    def __repr__(self):
        return self.__leaderboard

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
Name: merge_sort
Parameters: myList:list
Returns: list
Purpose: Sorts an unordered list into an ordered one
'''
def merge_sort(myList):
    list_length = len(myList)
    if list_length == 1:
        return myList
    mid_point = list_length // 2
    left = merge_sort(myList[:mid_point])
    right = merge_sort(myList[mid_point:])
    return merge(left, right)

'''
Name: merge
Parameters: left:list, right:list
Returns: output:list
Purpose: Sorts and merges two separate lists
'''
def merge(left, right):
    output = []
    i,  j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            output.append(left[i])
            i += 1
        else:
            output.append(right[j])
            j += 1
    output.extend(left[i:])
    output.extend(right[j:])
    return output

'''
Name: getLeaderboard
Parameters: serverType:string, playerID:integer|None, serverKey:string|None, client=Client|None
Returns: leaderboard:dictionary|None
Purpose: Gets the current updated version of the leaderboard for the player to see
'''
def getLeaderboard(serverType, playerID=None, serverKey=None, client=None) -> dict|None:
   # print("GET LEADERBOARD BEING CALLED")
    leaderboard = None
    if serverType == "public":
      #  if client is None:
      #      raise Exception("None Type Error: client should be Client object type value, not NoneType")
      #  else:
      #      client.sendData({"type":"leaderGet"})
      #      return leaderboard
        leaderboard = requests.get(url="http://127.0.0.1:5000/publicLeaderCheck").json()
    #    print(leaderboard)
        return leaderboard["data"]
    elif serverType == "private":
        if serverKey is None:
            raise Exception("None Type Error: severKey should be string type value, not NoneType")
        else:
            jsonInfo = {
                "serverKey":serverKey,
                "playerID":playerID
            }
            leaderboard = requests.get("http://127.0.0.1:5000/privateLeaderCheck", json={jsonInfo}).json()
    #    print(leaderboard)
        return leaderboard["data"]
    else:
        raise ValueError("Server type must be either public or private")


'''
Name: getDirection
Parameters: player:object, mousePos: list[int]|None
Returns: MPVector:list[int]
Purpose: Gets the direction vector that the projectile needs to move in
'''
def getDirection(player, mousePos: list[int]|None = None) -> list:
    if mousePos is None:
        mousePos = pygame.mouse.get_pos()
    MPVector = [player.rect.x - mousePos[0], player.rect.y - mousePos[1]]
    try:
        hyppotenuse = math.sqrt((MPVector[0] ** 2) + (MPVector[1] ** 2))
        divider = hyppotenuse // 10
        for i in range(2):
            MPVector[i] //= divider
        return MPVector

    except ValueError:
        hyppotenuse = math.sqrt((MPVector[0] ** 2) + (MPVector[1] ** 2)+1)
        divider = hyppotenuse // 10
        for i in range(2):
            MPVector[i] //= divider
        return MPVector

    except ZeroDivisionError:
        hyppotenuse = math.sqrt((MPVector[0] ** 2) + (MPVector[1] ** 2) + 1)
        divider = (hyppotenuse // 10) + 2
        for i in range(2):
            MPVector[i] //= divider
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
    if clientPlayer.playerID - 1 == 0:
        platformInfo = sendPlatformInfo(platforms)
        platformInfoDict = {"type": "platformInfo", "data": platformInfo}
        print(platformInfoDict)
        client.sendData(platformInfoDict)

'''
Name: data_handling
Parameters: data:str
Returns: list[dict]
Purpose: Handles what should happen with the data initially, just to help avoid extra data errors
'''
def data_handling(data:str) -> list[dict]:
    try:
        msgList: list[str] = data.split("}")

        returnList: list[dict] = []

        while '' in msgList:
            msgList.remove('')

        for i in range(len(msgList)):
            noDicts: int = 0
            temp: str = msgList[i]

            for letter in temp:
                if letter == '{':
                    noDicts += 1
            temp += '}' * noDicts

            returnList.append(dict(json.loads(temp)))

        return returnList

    except Exception as e:
        print("Error", e)

if __name__ == "__main__":
    pass
