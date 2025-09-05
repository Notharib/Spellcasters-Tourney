from basePlatform import Platform

'''
Name: generateSpawnPoints
Parameters: platformPositions:list
Returns: spawnPoints:list
Purpose: Generates the spawnPoints for the server to use
'''
def generateSpawnPoints(platformPositions: list) -> list:
    spawnPoints: list = []
    for i in range(len(platformPositions)):
        spawnPoints.append((platformPositions[i][0], platformPositions[i][1]+20))
    return spawnPoints


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
