import math

gravityConstant: float = 9.807
airDensity: float = 1.225

# Free falling equations

'''
Name: timeConstant 
Parameters: mass: int, dragCoef: float, area: float
Returns: float
Purpose: Generates the time constant needed for calculating the velocity
'''
def timeConstant(mass: int, dragCoef: float, area: float) -> float:
    global airDensity
    return mass / (dragCoef * area * airDensity)

'''
Name: terminalVelocity
Parameters: mass: int, dragCoef: float, area: float, timeCons: float
Returns: float
Purpose: Generates the terminal velocity of an object based off of the parameters
'''
def terminalVelocity(mass: int, dragCoef: float, area: float, timeCons: float) -> float:
    global gravityConstant
    return math.sqrt(2* gravityConstant * timeCons)

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