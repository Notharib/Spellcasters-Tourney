import math

from enum import Enum

'''
Name: Constants
Purpose: Enumerates the physics constants to be used throughout the program
'''
class Constants(Enum):
    GRAVITY: float = 9.807
    AIRDENSITY: float = 1.225

# Free falling equations

'''
Name: timeConstant 
Parameters: mass: int, dragCoef: float, area: float
Returns: float
Purpose: Generates the time constant needed for calculating the velocity
'''
def timeConstant(mass: int, dragCoef: float, area: float) -> float:
    return mass / (dragCoef * area * Constants.AIRDENSITY.value)

'''
Name: terminalVelocity
Parameters: mass: int, dragCoef: float, area: float, timeCons: float
Returns: float
Purpose: Generates the terminal velocity of an object based off of the parameters
'''
def terminalVelocity(mass: int, dragCoef: float, area: float, timeCons: float) -> float:
    return math.sqrt(2* Constants.GRAVITY.value * timeCons)

def averageVelocity(mass: int, dragCoef: float, area: float):
    '''
    Name: averageVelocity
    Parameters: mass: int, dragCoef: float, area: float
    Returns: lambda
    Purpose: Returns a lambda function that will approximate what the velocity of
    an object should be based upon how long it has been falling
    '''
    TIMC: float = timeConstant(mass, dragCoef, area)
    return lambda time : terminalVelocity(mass, dragCoef, area, TIMC) * (1 - (TIMC / time) * (1 - math.exp(-time / TIMC)))

'''
Name: projectileSpeed
Parameters: position: int, timeMoving: int, acceleration: float
Returns: int
Purpose: Uses the SUVAT equation to figure out what the current 
'''
def projectileSpeed(position: int, timeMoving: int, acceleration: float = Constants.GRAVITY.value) -> int:
    return round(position + 0.5 * acceleration * (timeMoving**2)) // timeMoving