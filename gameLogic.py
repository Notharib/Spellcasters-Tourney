import pygame, math, requests, unittest, random, json



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
Purpose: Handles what should initially happen with data,
to avoid extra data errors
'''
def data_handling(data: str) -> list[dict]:
    try:
        if '}{' in data:
            msgList: list[str] = data.split("}{")

            returnList: list[dict] = []

            temp: str = ""

            for i in range(len(msgList)):
                if i == 0:
                    temp = msgList[0] + '}'
                    returnList.append(dict(json.loads(temp)))
                elif i == len(msgList) -1:
                    temp = '{' + msgList[i]
                    returnList.append(dict(json.loads(temp)))
                else:
                    temp = '{' + msgList[i] + '}'
                    returnList.append(dict(json.loads(temp)))

            return returnList
        
        else:
            return [dict(json.loads(data))]
            
    except Exception as e:
        print("Data Handling Error:", e)

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
