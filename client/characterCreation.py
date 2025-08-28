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
        self._strength str = ""
        self._weakness: str = ""

    '''
    Name: getType
    Parameters: None
    Returns: self._type:str
    Purpose: Getter for the type variable
    '''
    def getType(self) -> str:
        return self._type

    '''
    Name: getWeakness
    Parameters: None
    Returns: self._weakness
    Purpose: Getter for the element type that this element
    takes more damage from
    '''
    def getWeakness(self) -> str: 
        return self._weakness

    '''
    Name: getStrength
    Parameters: None
    Returns: self._strength
    Purpose: Getter for the element type that this element
    does more damage to
    '''
    def getStrength(self) -> str:
        return self._strength

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
