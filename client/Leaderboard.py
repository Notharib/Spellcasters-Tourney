import requests
import pygame

from gameLogic import merge_sort

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
    def __init__(self) -> None:
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
    def update(self, leaderboard: dict) -> None:
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

        orderedDeath = merge_sort(deathValues)

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
Name: getLeaderboard
Parameters: serverType:string, playerID:integer|None, serverKey:string|None, client=Client|None
Returns: leaderboard:dictionary|None
Purpose: Gets the current updated version of the leaderboard for the player to see
'''
def getLeaderboard(serverType, playerID=None, serverKey=None, client=None):
    leaderboard = None
    if serverType == "public":
      leaderboard = requests.get(url="http://127.0.0.1:5000/publicLeaderCheck").json()
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

            return leaderboard["data"]
    else:
        raise ValueError("Server type must be either public or private")
