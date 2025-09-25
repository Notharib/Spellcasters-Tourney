class Queue:
    '''
    Name: Queue
    Purpose: To handle the functions of a queue data type
    '''
    def __init__(self) -> None:
        '''
        Name: __init__
        Parameters: self
        Returns: None
        Description: Initialises the Queue as a list with 10 Null elements and
        initialises the rear to -1
        '''
        self.__data: list = [None for i in range(10)]
        self.__back: int = -1

    def dumpData(self) -> None:
        '''
        Name: dumpData
        Parameters: self
        Returns: None
        Description: Used in unit tests to dump any leftover data from a previous test
        '''
        self.__data = [None for i in range(10)]
        self.__back = -1

    def loadData(self) -> None:
        '''
        Name: loadData
        Parameters: self
        Returns: None
        Description: Used in the unit tests just to generate random data to be used
        '''
        self.__data = [random.randint(0,100) for i in range(10)]
        self.__back = 9

    def getFront(self):
        '''
        Name: getFront
        Parameters: self
        Returns: None
        Description: Returns the front element of the queue
        '''
        return self.__data[0]

    def getBack(self):
        '''
        Name: getBack
        Parameters: self
        Returns: self._data[self.__back]
        Description: Checks if the Queue is full, if not adds new element
        to the rear of the Queue and updates the rear pointer
        '''
        if not self.is_empty():
            return self.__data[self.__back]
        else:
            raise Exception("Attempted to get back of an empty queue")

    def enqueue(self, data) -> None:
        '''
        Name: enqueue
        Parameters: self, data
        Returns: None
        Description: Checks if the Queue is full, if not adds new element
        to the rear of the Queue and updates the rear pointer
        '''
        if not self.is_full():
            if self.__back == -1:
                self.__data[0] = data
                self.__back = 0
            else:
                self.__back += 1
                self.__data[self.__back] = data
        else:
            raise Exception("Attempted to enter data into a queue that is full")

    def dequeue(self):
        '''
        Name: dequeue
        Parameters: self
        Returns: String|Integer|Dictionary
        Description: Returns the item at
        the front of the Queue and updates the front pointer
        '''
        if not self.is_empty():
            org = self.__data[0]

            self.__data.pop(0)
            self.__data.append(None)

            noneValues = 0
            for item in self.__data:
                if item is None:
                    noneValues += 1
            if noneValues == 10:
                self.__back = -1

            return org
        else:
            raise Exception("Attempted to dequeue an empty queue")

    def is_full(self) -> bool:
        '''
        Name: isfull
        Parameters: Self
        Returns: Boolean
        Description: Returns True if the Queue is full and False if not
        '''
        return self.__back == 9

    def is_empty(self) -> bool:
        '''
        Name: is_empty
        Parameters: Self
        Returns: Boolean
        Description: Returns True if the Queue is empty and False if not
        '''
        return self.__back == -1

    def spaces_free(self) -> int:
        '''
        Name: spaces_free
        Parameters: Self
        Returns: Integer
        Description: Returns how many empty spaces remain in the Queue
        '''
        noneValues: int = 0
        for item in self.__data:
            if item is None:
                noneValues += 1

        return noneValues