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
    def __init__(self):
        self.__opposite = "Water"
        self.__type = "Fire"

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

# Spellcaster Classes

'''
Name: Wizard
Purpose: To handle properties of the wizard spellcaster
'''
class Wizard:
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Wizard object
    '''
    def __init__(self):
        self.__type = "Wizard"

'''
Name: Druid
Purpose: To handle properties of the druid spellcaster
'''
class Druid:
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Druid object
    '''
    def __init__(self):
        self.__type = "Druid"