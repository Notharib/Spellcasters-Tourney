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
    def setUp(self):
        self.leaderboard = gameLogic.Leaderboard()

        for i in range(3):
            randomPlayer = [random.randint(0,100),random.randint(0,100)]
            self.leaderboard.addToLeader(randomPlayer)
    '''
    Name: test_isLeaderboardGetter
    Parameters: None
    Returns: None
    Purpose: Unit test to make sure the leaderboard is returning as a dictionary
    '''
    def test_isLeaderboardGetter(self):
        self.assertEqual(type(self.leaderboard.getLeaderboard()),type({}),"Problem with Leaderboard getter or variable")

    '''
    Name: test_isDisplayTextGetter
    Parameters: None
    Returns: None
    Purpose: Unit test to make sure the display text getter is returning a string
    '''
    def test_isDisplayTextGetter(self):
        self.assertEqual(type(self.leaderboard.getDisplayText()),type("Hello World"), "Problem with DisplayText getter or variable")

    '''
    Name: test_LeaderStructure
    Parameters: None
    Returns: None
    Purpose: Unit test to make sure the leaderboard is structuring properly
    '''
    def test_LeaderStructure(self):
        orderedDeath = self.leaderboard.setupLeaderStructure()
        self.assertGreater(len(orderedDeath),0)
        for item in orderedDeath:
            self.assertEqual(type(item),type([]))


class linearQueueTesting(unittest.TestCase):
    
    def setUp(self):
        self.linearQueue = gameLogic.queue()

    
    def test_empty(self):
        self.linearQueue.dumpData()
        self.assertTrue(self.linearQueue.isempty())

    
    def test_full(self):
        self.linearQueue.dumpData()
        self.linearQueue.loadData()
        self.assertTrue(self.linearQueue.isfull())

    
    def test_enqueue(self):
       # All data that may be left over from another test is dumped 
        self.linearQueue.dumpData()
        # Enqueuing some data to test it
        self.linearQueue.enqueue(5)
        self.linearQueue.enqueue(100)
        self.linearQueue.enqueue(76)
        
        # The test itself
        self.assertEqual(self.linearQueue.getBack(),76)

    
    def test_dequeue(self):
        # Dumping old leftover data. and then inserting new data into the queue
        self.linearQueue.dumpData()
        self.linearQueue.loadData()
        
        actualFront = self.linearQueue.getFront()
        testFront = self.linearQueue.dequeue()

        self.assertEqual(actualFront, testFront)

    
    def test_freeSpaces(self):
        self.linearQueue.dumpData()
        self.assertEqual(10, self.linearQueue.spaces_free())

        repetitions = random.randint(1,9)
        for i in range(repetitions):
            self.linearQueue.enqueue(random.randint(1,100))
        theoreticalFree = 10 - repetitions
        self.assertEqual(theoreticalFree, self.linearQueue.spaces_free())

        self.linearQueue.dumpData()
        self.linearQueue.loadData()

        self.assertEqual(0, self.linearQueue.spaces_free())

if __name__ == "__main__":
    unittest.main()
