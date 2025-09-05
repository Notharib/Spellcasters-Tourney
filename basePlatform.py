

'''
Name: Platform
Purpose: To have platforms that players are able to move around on
'''
class Platform:
    '''
    Name: __init__
    Parameters: position: list, size:list
    Returns: None
    Purpose: Constructor to set the initial values
    of the platform object
    '''
    def __init__(self, position, size=[20,500]):
        self.__position = position
        self.__size = size
        self.__colour = (0,0,255)
        self.__top = None
        self.__left = None
        self.__right = None
        self.__bottom = None
    # Getters and Setters

    '''
    Name: getPos
    Parameters: None
    Returns: self.__position:list
    Purpose: Getter for self.__position
    '''
    def getPos(self):
        return self.__position

    '''
    Name: getPos
    Parameters: None
    Returns: self.__size:list
    Purpose: Getter for self.__size
    '''
    def getSize(self):
        return self.__size

    '''
    Name: getTop
    Parameters: None
    Returns: self.__top
    Purpose: Getter for self.__top
    '''
    def getTop(self):
        return self.__top

    '''
    Name: getBottom
    Parameters: None
    Returns: self.__bottom
    Purpose: Getter for self.__bottom
    '''
    def getBottom(self):
        return self.__bottom

    '''
    Name: getLeft
    Parameters: None
    Returns: self.__left
    Purpose: Getter for self.__left
    '''
    def getLeft(self):
        return self.__left

    '''
    Name: getRight
    Parameters: None
    Returns: self.__right
    Purpose: Getter for self.__right
    '''
    def getRight(self):
        return self.__right

    '''
    Name: setTop
    Parameters: top
    Returns: None
    Purpose: Setter for self.__top
    '''
    def setTop(self, top):
        self.__top = top
        return None

    '''
    Name: setLeft
    Parameters: left
    Returns: None
    Purpose: Setter for self.__left
    '''
    def setLeft(self, left):
        self.__left = left
        return None

    '''
    Name: setRight
    Parameters: right
    Returns: None
    Purpose: Setter for self.__right
    '''
    def setRight(self, right):
        self.__right = right
        return None

    ''' 
    Name: setBottom
    Parameters: bottom
    Returns: None
    Purpose: Setter for self.__bottom
    '''
    def setBottom(self, bottom):
        self.__bottom = bottom
        return None

    '''
    Name: __repr__
    Parameters: None
    Returns: self.__postion
    Purpose: Defines how this object should be represented if printed directly
    '''
    def __repr__(self):
        return self.__position
