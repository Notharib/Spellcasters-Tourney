import pygame, math, requests, unittest, random

# Non-player objects to be used within the game

class linearQueue:
    '''
    Name: __init__
    Parameters: self
    Returns: None
    Description: Initialises the Queue as a list with 10 Null elements and
    initialises the front and rear to -1
    '''
    def __init__(self):
        self.__data = [None, None, None, None, None, None, None, None, None, None]
        self.__front = -1
        self.__rear = -1

    '''
    Name: enqueue
    Parameters: self, newdata: String|Integer|Dictionary
    Returns: None
    Description: Checks if the Queue is full, if not adds new element
    to the rear of the Queue and updates the rear pointer
    '''
    def enqueue(self, newdata):
        if self.isempty():
            self.__rear = (self.__rear + 1) % len(self.__data)
            self.__data[self.__rear] = newdata
        if self.__front == -1:
            self.__front += 1

    '''
    Name: dequeue
    Parameters: self
    Returns: String|Integer|Dictionary
    Description: Returns the item at
    the front of the Queue and updates the front pointer
    ''' 
    def dequeue(self):
        val = self.__data[self.__front]
        if self.__front == self.__rear:
            self.__front, self.__rear = -1, -1
        else:
            self.__front = (self.__front + 1) % len(self.__data)
        return val

    '''
    Name: is_empty
    Parameters: Self
    Returns: Boolean
    Description: Returns True if the Queue is empty and False if not
    '''
    def isempty(self):
        if self.__front == -1:
            return True
        else:
            return False
    
    '''
    Name: is_full
    Parameters: Self
    Returns: Boolean
    Description: Returns True if the Queue is full and False if not
    '''
    def isfull(self):
        if self.__rear + 1 == self.__front or self.__front + 1 == self.__rear:
            return True
        else:
            return False

    '''
    Name: getFront
    Parameters: Self
    Returns: String|Integer|Dictionary
    Description: Returns whatever data is at the front of the queue
    '''
    def getFront(self):
        return self.__data[self.__front]

    '''
    Name: getBack
    Parameters: Self
    Returns: String|Integer|Dictionary
    Description: Returns whatever data is at the back of the queue
    '''
    def getBack(self):
        return self.__data[self.__rear]

    '''
    Name: spaces_free
    Parameters: Self
    Returns: Integer
    Description: Returns how many empty spaces remain in the Queue
    '''
    def spaces_free(self):
        if self.isempty():
            return len(self.__data)#
        elif self.isfull():
            return 0
        elif self.__front > self.__rear:
            return (self.__rear - self.__front) * -1
        elif self.__rear > self.__front:
            return (self.__front - self.__front) * -1
        else:
            return len(self.__data) -1

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
        self.__leaderboard = {}
        self.__displayText = ""
        self.X = 200
        self.Y = 0
        self.width = 400
        self.height = 300
        self.colour = (0,0,255)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image, self.colour, [self.X, self.Y, self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y

    '''
    Name: update
    Parameters: leaderboard:dictionary
    Returns: None
    Purpose: Updates the values of different variables within the class as needed
    '''
    def update(self, leaderboard):
        self.__displayText = ""
        self.__leaderboard = leaderboard
        leaderList = self.setupLeaderStructure()
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
    def getDisplayText(self):
        return self.__displayText

    '''
    Name: getLeaderboard 
    Parameters: None 
    Returns: dictionary 
    Purpose: Getter for the leaderboard variable
    '''    
    def getLeaderboard(self):
        return self.__leaderboard


    '''
    Name: addToLeader
    Parameters: examplePlayer:list
    Returns: None
    Purpose: Function only used for unit testing to add players to
    the leaderboard
    '''
    def addToLeader(self,examplePlayer):
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
Parameters: serverType:string, playerNo:integer|None, serverKey:string|None, client=Client|None
Returns: leaderboard:dictionary|None
Purpose: Gets the current updated version of the leaderboard for the player to see
'''
def getLeaderboard(serverType, playerNo=None, serverKey=None, client=None):
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
                "playerNo":playerNo
            }
            leaderboard = requests.get("http://127.0.0.1:5000/privateLeaderCheck", json={jsonInfo}).json()
    #    print(leaderboard)
        return leaderboard["data"]
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
