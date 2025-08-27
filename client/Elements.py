# Element Classes

'''
Name: Fire
Purpose: To handle properties to do with the fire element
'''
class Fire:
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Fire object
    '''
    def __init__(self) -> None:
        self.__opposite: str = "Water"
        self.__type: str = "Fire"

    '''
    Name: getType
    Parameters: None
    Returns: __type:str
    Purpose: Getter for the type variable
    '''
    def getType(self) -> str:
        return self.__type

    '''
    Name: getOpposite
    Parameters: None
    Returns: __opposite:str
    Purpose: Getter for the opposite variable
    '''
    def getOpposite(self) -> str:
        return self.__opposite

    '''
    Name: __repr__
    Parameters: None
    Returns: self.__type
    Purpose: Determines how the object should be represented if nothing is specified
    '''
    def __repr__(self):
        return self.__type

'''
Name: Water
Purpose: To handle properties to do with the water element
'''
class Water:
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Water object
    '''
    def __init__(self):
        self.__opposite = "Fire"
        self.__type = "Water"

    '''
    Name: __repr__
    Parameters: None
    Returns: self.__type
    Purpose: Determines how the object should be represented if nothing is specified
    '''
    def __repr__(self):
        return self.__type

