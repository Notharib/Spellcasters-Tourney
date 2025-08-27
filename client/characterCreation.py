import math

# Base Character Class

'''
Name: BaseCharacter
Purpose: Base Character class for other classes to
inherit from
'''
class BaseCharacter:

    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the BaseCharacter object
    '''
    def __init__(self) -> None:
        self._height: int = 40
        self._width: int = 40
        self._HP: int = 100
        self._timeSinceLastHit: int = -1
        self._RegenTime: int = -1
        self._Regeneration = lambda time: math.exp(time)
        self._Element = None
        self._Caster = None

    '''
    Name: takeDamage
    Parameters: damage:int
    Returns: None
    Purpose: Setter that adjusts the HP of the character
    '''
    def takeDamage(self, damage: int) -> None:
        self._HP -= damage

    '''
    Name: setCaster
    Parameters: casterType:object
    Returns: None
    Purpose: Setter that sets the caster variable
    '''
    def setCaster(self, casterType) -> None:
        self._Caster = casterType

    '''
    Name: setElement
    Parameters: elementType: object
    Returns: None
    Purpose: Setter for the element variable
    '''
    def setElement(self, elementType) -> None:
        self._Element = elementType

# Base Element Class

class Element: 
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Element object
    '''
    def __init__(self) -> None:
        self._type: str = ""
        self._oppositeType: str = ""

    '''
    Name: getType
    Parameters: None
    Returns: self._type:str
    Purpose: Getter for the type variable
    '''
    def getType(self) -> str:
        return self._type

    '''
    Name: getOpposite
    Parameters: None
    Returns: self._oppositeType
    Purpose: Getter for the opposite type
    variable
    '''
    def getOpposite(self) -> str: 
        return self._oppositeType

    '''
    Name: __repr__
    Parameters: None
    Returns: self._type:str
    Purpose: Repr for any of the elements
    '''
    def __repr__(self) -> str:
        return self._type



#Base Character Class

class Caster:
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Caster object
    '''
    def __init__(self) -> None:
        self._type: str = ""
   
    '''
    Name: ability
    Parameters: None
    Returns: None
    Purpose: Abstract method for where the
    Spellcaster's unique ability shall go
    '''
    def ability(self) -> None:
        pass

    '''
    Name: altAttack
    Parameters: None
    Returns: None
    Purpose: Abstract method for where the
    Spellcaster's unique alternate attack
    shall go
    '''
    def altAttack(self) -> None:
        pass

    '''
    Name: __repr__
    Parameters: None
    Returns: self._type:str
    Purpose: Repr for the Caster object
    '''
    def __repr__(self) -> str:
        return self._type
