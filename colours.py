from enum import Enum

'''
Name: Colours
Purpose: Enumarates the Colour constants to be used in the program
'''
class Colours(Enum):
    RED: tuple[int,int,int] = (250, 9, 1)
    GREEN: tuple[int,int,int] = (2, 249, 0)
    BLUE: tuple[int,int,int] = (0, 0, 240)
    PURPLE: tuple[int,int,int] = (160, 32, 240)
    WHITE: tuple[int,int,int] = (255,255,255)
    BLACK: tuple[int, int, int] = (0,0,0)