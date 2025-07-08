import unittest, random
import gameLogic, client, menuClasses, PrivateServer

# gameLogic Unit Tests

'''
Name: LeaderboardTesting
Inherits: unittest.TestCase
Purpose: Unit test for the leaderboard class and all of its functions
'''
class LeaderboardTesting(unittest.TestCase):
    '''
    Name: setUp
    Parameters: None
    Returns: None
    Purpose: Sets up the unit test
    '''
    def setUp(self) -> None:
        self.leaderboard: gameLogic.Leaderboard = gameLogic.Leaderboard()

        for i in range(3):
            randomPlayer: list[int] = [random.randint(0,100),random.randint(0,100)]
            self.leaderboard.addToLeader(randomPlayer)
    '''
    Name: test_isLeaderboardGetter
    Parameters: None
    Returns: None
    Purpose: Unit test to make sure the leaderboard is returning as a dictionary
    '''
    def test_isLeaderboardGetter(self) -> None:
        self.assertEqual(type(self.leaderboard.getLeaderboard()),type({}),"Problem with Leaderboard getter or variable")

    '''
    Name: test_isDisplayTextGetter
    Parameters: None
    Returns: None
    Purpose: Unit test to make sure the display text getter is returning a string
    '''
    def test_isDisplayTextGetter(self) -> None:
        self.assertEqual(type(self.leaderboard.getDisplayText()),type("Hello World"), "Problem with DisplayText getter or variable")

    '''
    Name: test_LeaderStructure
    Parameters: None
    Returns: None
    Purpose: Unit test to make sure the leaderboard is structuring properly
    '''
    def test_LeaderStructure(self) -> None:
        orderedDeath = self.leaderboard.setupLeaderStructure()
        self.assertGreater(len(orderedDeath),0)
        for item in orderedDeath:
            self.assertEqual(type(item),type([]))

'''
Name: QueueTesting
Inherits: unittest.TestCase
Purpose: Unit test for the Queue class and all its functions 
'''
class QueueTesting(unittest.TestCase):
    
    def setUp(self) -> None:
        '''
        Name: setUp
        Parameters: None
        Returns: None
        Purpose: Sets up the unit test
        '''
        self.queue: gameLogic.queue = gameLogic.queue()

    def test_empty(self) -> None:
        '''
        Name: test_empty
        Parameters: None
        Returns: None
        Purpose: Unit test to ensure the queue is able to test whether it is empty properly
        '''
        self.queue.dumpData()
        self.assertTrue(self.queue.is_empty())

    def test_full(self) -> None:
        '''
        Name: test_full
        Parameters: None
        Returns: None
        Purpose: Unit test to ensure the queue is able to test whether it is full properly
        '''
        self.queue.dumpData()
        self.queue.loadData()
        self.assertTrue(self.queue.is_full())

    def test_enqueue(self) -> None:
        '''
        Name: test_enqueue
        Parameters: None
        Returns: None
        Purpose: Unit test to ensure the enqueue function is working as intended
        '''
       # All data that may be left over from another test is dumped 
        self.queue.dumpData()
        # Enqueuing some data to test it
        self.queue.enqueue(5)
        self.queue.enqueue(100)
        self.queue.enqueue(76)
        
        # The test itself
        self.assertEqual(self.queue.getBack(),76)

    
    def test_dequeue(self) -> None:
        '''
        Name: test_dequeue
        Parameters: None
        Returns: None
        Purpose: Unit test to ensure that the dequeue function is working as intended
        '''
        # Dumping old leftover data. and then inserting new data into the queue
        self.queue.dumpData()
        self.queue.loadData()
        
        actualFront = self.queue.getFront()
        testFront = self.queue.dequeue()

        self.assertEqual(actualFront, testFront)
    
    def test_freeSpaces(self) -> None:
        '''
        Name: test_freeSpaces
        Parameters: None
        Returns: None
        Purpose: Unit test to ensure the freeSpaces function is working as intended
        '''
        self.queue.dumpData()
        self.assertEqual(10, self.queue.spaces_free())

        repetitions: int = random.randint(1,9)
        for i in range(repetitions):
            self.queue.enqueue(random.randint(1,100))
        theoreticalFree: int = 10 - repetitions
        self.assertEqual(theoreticalFree, self.queue.spaces_free())

        self.queue.dumpData()
        self.queue.loadData()

        self.assertEqual(0, self.queue.spaces_free())

# client unit tests



# menuClsses unit tests

if __name__ == "__main__":
    unittest.main()
