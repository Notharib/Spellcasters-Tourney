from characterCreation import Element

# Element Classes

'''
Name: Fire
Purpose: To handle properties to do with the fire element
'''
class Fire(Element):
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Fire object
    '''
    def __init__(self) -> None:
        super().__init__()
        self._oppositeType: str = "Water"
        self._type: str = "Fire"
        self._strength: str = "Earth"

'''
Name: Water
Purpose: To handle properties to do with the water element
'''
class Water(Element):
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Water object
    '''
    def __init__(self) -> None:
        super().__init__()
        self._weakness: str = "Earth"
        self._type: str = "Water"
        self._strength: str = "Fire"

