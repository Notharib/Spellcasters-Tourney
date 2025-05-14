import random

def IPToHash(IP):
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

    return {"hashedItem":hashedItem}

def fullServer(fullValue):
    if fullValue == 1:
        return True
    elif fullValue == 0:
        return False
    else:
        raise ValueError("fullValue should either be 1 or 0")