import pygame
import math
import requests
import unittest
import random
import json



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


# General functions

class Queue:
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
    if clientPlayer.getPlayerID() - 1 == 0:
        platformInfo = sendPlatformInfo(platforms)
        platformInfoDict = {"type": "platformInfo", "data": platformInfo}
        print(platformInfoDict)
        client.sendData(platformInfoDict)

'''
Name: data_handling
Parameters: data:str
Returns: list[dict]
Purpose: Handles what should initially happen with JSON data, 
to avoid extra data errors
'''
def data_handling(data: str) -> list[dict]:
    try: 
        
        decoder = json.JSONDecoder()
        iterator: int = 0
        retVal: list[dict] = []

        while iterator < len(data):
            data = data.lstrip()
            msg, offset = decoder.raw_decode(data[iterator:])
            retVal.append(msg)
            iterator += offset

        return retVal

    except SyntaxError as e:
        print("Data Handling Syntax Error:",e)

    except json.JSONDecodeError as e:
        print("Data Handling JSON Error:",e)

    except Exception as e:
        print("Data Handling Error:", e)
        print("Origin Message:", data)

# Unit Tests
class LeaderboardTesting(unittest.TestCase):
    '''
    Name: setUp
    Parameters: None
    Returns: None
    Purpose: Sets up the unit test
    '''
    def setUp(self):
        self.leaderboard = Leaderboard()
        
        for i in range(3):
            randomPlayer = [random.randint(0,100),random.randint(0,100)]
            self.leaderboard.addToLeader(randomPlayer)

    '''
    Name: test_isLeaderboardGetter
    Parameters: None
    Returns: None
    Purpose: Unit test to make sure the leaderboard is returning as a dictionary
    '''
    def test_isLeaderboardGetter(self):
        self.assertEqual(type(self.leaderboard.getLeaderboard()),type({}),"Problem with Leaderboard getter or variable")
    
    '''
    Name: test_isDisplayTextGetter
    Parameters: None
    Returns: None
    Purpose: Unit test to make sure the display text getter is returning a string
    '''
    def test_isDisplayTextGetter(self):
        self.assertEqual(type(self.leaderboard.getDisplayText()),type("Hello World"), "Problem with DisplayText getter or variable")
    
    '''
    Name: test_LeaderStructure
    Parameters: None
    Returns: None
    Purpose: Unit test to make sure the leaderboard is structuring properly
    '''
    def test_LeaderStructure(self):
        orderedDeath = self.leaderboard.setupLeaderStructure()
        self.assertGreater(len(orderedDeath),0)
        for item in orderedDeath:
            self.assertEqual(type(item),type([]))


if __name__ == "__main__":
    unittest.main()
