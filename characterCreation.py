import math

from abc import abstractmethod

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
        self._type: str
        self._strength: str
        self._weakness: str
        self._ability: str

    '''
    Name: getAbility
    Parameters: None
    Returns: self._ability: str
    Purpose: Getter for the ability variable
    '''
    def getAbility(self) -> str:
        return self._ability

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
        self._type: str
        self._ability: str
        self._HP: int
    
    '''
    Name: getHP
    Parameters: None
    Returns self._HP: int
    Purpose: Getter for the caster's HP
    '''
    def getHP(self) -> int:
        return self._HP

    '''
    Name: getAbility
    Parameters: None
    Returns: str
    Purpose: Getter for the casters's unique ability
    '''
    def getAbility(self) -> str:
        # Short for regeneration (will double the Druid's base regeneration)
        return self._ability

    '''
    Name: altAttack
    Parameters: None
    Returns: None
    Purpose: Abstract method for where the
    Spellcaster's unique alternate attack
    shall go
    '''
    @abstractmethod
    def altAttack(self) -> None:
        pass

    '''
    Name: getType
    Parameters: None
    Returns: self._type:str
    Purpose: Getter for the type variable
    '''
    def getType(self) -> str:
        return self._type

    '''
    Name: __repr__
    Parameters: None
    Returns: self._type:str
    Purpose: Repr for the Caster object
    '''
    def __repr__(self) -> str:
        return self._type