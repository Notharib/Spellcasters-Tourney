import math
import requests
import unittest
import random
import json
import pygame

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
