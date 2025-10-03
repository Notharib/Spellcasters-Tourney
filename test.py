import math
import random
import unittest

from time import sleep

import Leaderboard
import gameLogic
import dataStructures
import client


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
        self.leaderboard: Leaderboard.Leaderboard = Leaderboard.Leaderboard()

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
        self.queue: dataStructures.Queue = dataStructures.Queue()

    def loadQueue(self) -> None:
        '''
        Name: loadQueue
        Parameters: None
        Returns: None
        Purpose: Loads some random data into the queue
        '''
        for i in range(10):
            self.queue.enqueue(random.randint(1,100))

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
        self.loadQueue()
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

        self.loadQueue()
        
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
        self.loadQueue()

        self.assertEqual(0, self.queue.spaces_free())


def getActualMousePos(player:client.Character, mousePos:list[int]) -> list[int]:
    '''
    Name: getActualMousePos
    Parameters: player:client.Character, mousePos:list[int]
    Returns: MPVector:list[int]
    Purpose: Function just to check that the vector is functioning as intended
    '''
    MPVector = [player.rect.x - mousePos[0], player.rect.y - mousePos[1]]
    try:
        hyppotenuse = math.sqrt((MPVector[0] ** 2) + (MPVector[1] ** 2))
        divider = hyppotenuse // 10
        for i in range(2):
            MPVector[i] //= divider
        return MPVector
    except ValueError:
        hyppotenuse = math.sqrt((MPVector[0] ** 2) + (MPVector[1] ** 2) + 1)
        divider = hyppotenuse // 10
        for i in range(2):
            MPVector[i] //= divider
        return MPVector

    except ZeroDivisionError:
        hyppotenuse = math.sqrt((MPVector[0] ** 2) + (MPVector[1] ** 2) + 1)
        divider = (hyppotenuse // 10) + 2
        for i in range(2):
            MPVector[i] //= divider
        return MPVector

'''
Name: getDirTetsts
Inherits: unittest.TestCase
Purpose: Unit test for the projectile direction generator
'''
class getDirTests(unittest.TestCase):
    def setUp(self) -> None:
        '''
        Name: setUp
        Parameters: None
        Returns: None
        Purpose: Set up the unit test
        '''
        self.player = client.Character([200,200], (0,255,100), 2)

    def test_acceptableDirection(self) -> None:
        '''
        Name: test_acceptableDirection
        Parameters: None
        Returns: None
        Purpose: Unit test to an acceptable case
        '''
        mousePos = [random.randint(1,self.player.X-10) for i in range(2)]
        MPVector = gameLogic.getDirection(self.player, mousePos)
        self.assertEqual(MPVector, getActualMousePos(self.player, mousePos))

    def test_edgeCase(self) -> None:
        '''
        Name: test_edgeCase
        Parameters: None
        Returns: None
        Purpose: Unit test to test a potential edge case
        '''
        mousePos = [self.player.X -1, self.player.X -1]
        MPVector = gameLogic.getDirection(self.player, mousePos)
        self.assertEqual(MPVector, getActualMousePos(self.player, mousePos))

    def test_Zero(self) -> None:
        '''
        Name: test_Zero
        Parameters: None
        Returns: None
        Purpose: Unit test to test that the function is able to handle when there is no difference
        between the mouse pos and the player position
        '''
        mousePos = [self.player.X, self.player.Y]
        MPVector = gameLogic.getDirection(self.player, mousePos)
        self.assertEqual(MPVector, getActualMousePos(self.player, mousePos))

    def test_NegativeX(self) -> None:
        '''
        Name: test_NegativeX
        Parameters: None
        Returns: None
        Purpose: Unit test to test what happens when the mousePosX is negative
        '''
        mousePos = [-self.player.X, self.player.Y]
        MPVector = gameLogic.getDirection(self.player, mousePos)
        self.assertEqual(MPVector, getActualMousePos(self.player, mousePos))

    def test_NegativeY(self) -> None:
        '''
        Name: test_NegativeY
        Parameters: None
        Returns: None
        Purpose: Unit test to test what happens when the mousePosY is negative
        '''
        mousePos = [self.player.X, self.player.Y]
        MPVector = gameLogic.getDirection(self.player, mousePos)
        self.assertEqual(MPVector, getActualMousePos(self.player, mousePos))


# character tests

'''
Name: characterTesting
Inherits: unittest.TestCase
Purpose: Unit tests for the character class
'''
class characterTesting(unittest.TestCase): 
    '''
    Name: setUp
    Parameters: None
    Returns: None
    Purpose: Sets up the inital data for the unit tests 
    '''
    def setUp(self) -> None:
        self.initialPosition: list[int] = [random.randint(1,500), random.randint(1,500)]

        while self.initialPosition[0] == self.initialPosition[1]:
            self.initialPosition[1] = random.randint(1,500)

        self.initialColour: tuple[int,int,int] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.playerID: int = random.randint(1,10)

        self.character = client.Character(self.initialPosition, self.initialColour, self.playerID)

    '''
    Name: test_correctInitialPosition
    Parameters: None
    Returns: None
    Purpose: Unit test to test that the character's initial
    position generates correctly
    '''
    def test_correctInitialPosition(self) -> None:
        gottenPos: list[int] = self.character.getPos()
        self.assertEqual(gottenPos[0], self.initialPosition[0])
        self.assertEqual(gottenPos[1], self.initialPosition[1])

    '''
    Name: test_playerID
    Parameters: None
    Returns: None
    Purpose: Unit test to test whether the player's
    player ID set itself correctly
    '''
    def test_playerID(self) -> None:
        gottenID: int = self.character.getPlayerID()
        self.assertEqual(gottenID, self.playerID)
    
    '''
    Name: test_colour
    Parameters: None
    Returns: None
    Purpose: Unit test to test whether the character's initial
    colour sets correctly
    '''
    def test_colour(self) -> None:
        self.assertEqual(self.character.colour[0], self.initialColour[0])
        self.assertEqual(self.character.colour[1], self.initialColour[1])
        self.assertEqual(self.character.colour[2], self.initialColour[2])
    
    '''
    Name: test_changePos
    Parameters: None
    Returns: None
    Purpose: Unit test to test that after changing the character's
    position, it adjusts appropriately
    '''
    def test_changePos(self) -> None:
        adjuster: int = random.randint(1,50)
        
        self.character.rect.x -= adjuster
        self.character.rect.y -= adjuster

        gottenPos: list[int] = self.character.getPos()

        self.assertNotEqual(gottenPos[0], self.initialPosition[0])
        self.assertNotEqual(gottenPos[1], self.initialPosition[1])

        self.assertEqual(gottenPos[0]+adjuster, self.initialPosition[0])
        self.assertEqual(gottenPos[1]+adjuster, self.initialPosition[1])

        
# sorting algorithm tests

class mergeSortTest(unittest.TestCase):
    '''
    Name: test_almostSorted
    Parameters: None
    Returns: None
    Purpose: Unit test for a list that is almost sorted
    '''
    def test_almostSorted(self) -> None:
        data: list[int] = [1,2,3,4,8,6,5,10]

        sortedData: list[int] = gameLogic.merge_sort(data)

        for i in range(len(data)):
            if i == 0: 
                continue
            else:
                self.assertGreater(sortedData[i], sortedData[i-1])
    
    '''
    Name: test_randomData
    Parameters: None
    Returns: None
    Purpose: Unit test for completely random data
    in a list
    '''
    def test_randomData(self) -> None:
        data: list[int] = [random.randint(1,100) for i in range(100)]

        sortedData: list[int] = gameLogic.merge_sort(data)

        for i in range(len(data)):
            if i == 0:
                continue
            elif sortedData[i] == sortedData[i-1]:
                continue
            else:
                self.assertGreater(sortedData[i], sortedData[i-1])

    '''
    Name: test_largeNoOfData
    Parameters: None
    Returns: None
    Purpose: Tests whether it can sort a large list (>100 items) of data
    '''
    def test_largeNoOfData(self)-> None:
        data: list[int] = [random.randint(1,100) for i in range(150)]

        sortedData: list[int] = gameLogic.merge_sort(data)

        for i in range(len(data)):
            if i == 0:
                continue
            elif sortedData[i] == sortedData[i-1]:
                continue
            else:
                self.assertGreater(sortedData[i], sortedData[i-1])
        


if __name__ == "__main__":
    unittest.main()
