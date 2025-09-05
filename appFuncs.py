import random

'''
Name: IPToHash
Parameters: IP:string
Returns: dictionary
Purpose: Converts the IP address passed in, into a hashed key
'''
def IPToHash(IP: str) -> dict:
    numberList = []
    hashedItem = ""

    for i in range(len(IP)//2):
        if i % 2 == 0:
            numberList.append(random.randint(65,90))
        else:
            numberList.append(random.randint(97,122))

    for num in numberList:
        ch = chr(num)
        hashedItem += ch

    pin = ""
    for i in range(5):
        number = str(random.randint(0,9))
        pin += number

    pin = int(pin)

    return {"hashedItem":hashedItem, "PIN": pin}

'''
    Name: fullServer
    Parameters: fullValue:integer
    Returns: boolean
    Purpose: Determines whether the server is full or not based upon whether the fullValue is 1 or 0, and
    raises an error if it isn't either of those things 
    '''
def fullServer(fullValue: int) -> bool:
    if fullValue == 1:
        return True
    elif fullValue == 0:
        return False
    else:
        raise ValueError("fullValue should either be 1 or 0")

'''
Name: createPlayerID
Parameters: playerInfo: dictionary, playerIDs:list
Returns: dictionary
Purpose: Creates a unique player ID based upon information about the player
'''
def createPlayerID(playerInfo:dict, playerIDs:list) -> dict|None:
    playerID = playerInfo["playerID"]
    serverOrg = playerInfo[""]

if __name__ == "__main__":
    pass