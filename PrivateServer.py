import json
import socket
import threading
import time
from random import choice, randint

from gameLogic import data_handling
from serverClasses import Server, Client
from basePlatform import Platform

'''
Name: Server
Purpose: Server class to handle connections from the different clients. Different to the public server's
Server class, due to the differences in functionality required from both of them
'''
class PrivateServer(Server):
    '''
    Name: __init__
    Parameters: maxClients:integer, lengthOfGame:integer
    Returns: None
    Purpose: Constructor to set the initial values
    of the Server object
    '''
    def __init__(self, maxClients:int, lengthOfGame:int) -> None:
        Server.__init__(self,host=socket.gethostbyname(socket.gethostname()), port=50001, maxClients=maxClients)
        self.__lengthOfGame: int = int(lengthOfGame)
        self.__password: None|str = None
        self.__beginTime: None|int|float = None
        self.__waiting: int = 0

    '''
    Name: start
    Parameters: None
    Returns: None
    Purpose: Starts listening for connections from different clients. Will only accept connections
    until it reaches the amount of clients connected as pre-determined on the creation of the object
    '''
    def start(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self._HOST, self._PORT))
            s.listen(1)
            print("Server Setup and listening on port", self._PORT)
            print(self._maxClients)

            # Should only accept new connections while the length of the client lists is less than the max number of connections
            while len(self._clientList) < self._maxClients:
                conn, addr = s.accept()
                print("New Connection from ", addr)

                colour = (randint(0, 255), randint(0, 255), randint(0, 255))
                position = choice(self.__spawnPoints)

                time.sleep(0.1)
                self._clientList.append(Client(conn, choice(self._spawnPoints),len(self._clientList) + 1, colour))
                print(len(self._clientList))
                # Separate function used so that it will still continue running after the while loop in this function stops running
                self.startListening(conn)
                # Once the required number of clients has joined, send the start information to all the clients in '__clientList'
            print("Beginning Game!")
            self.beginGame()

    '''
    Name: startListening
    Parameters: conn:object
    Returns: None
    Purpose: Creates a thread that will begin listening for messages from the connection passed into
    the function
    '''
    def startListening(self, conn) -> None:
        threading.Thread(target=self.recv_from_client, args=(conn,)).start()

    '''
    Name: preStartChecks
    Parameters: None
    Returns: None
    Purpose: Runs the necessary checks before beginning the game
    '''
    def preStartChecks(self) -> None:
        idToPos: dict = {}
        iteration: int = 0

        for client in self._clientList:
            
            clientID: int = client.getPlayerID()
            idToPos[clientID] = iteration
            iteration += 1

            if client.getElement() is None:
                self.__waiting += 1

                msgDict: dict = {
                            "type": "missingElement",
                            "data": "Server Missing Client Element"
                        }
                client.sendData(json.dumps(msgDict))
                
            if client.getCaster() is None:
                self.__waiting += 1

                msgDict: dict = {
                            "type": "missingCaster",
                            "data": "Server Missing Client Caster"
                        }

                client.sendData(json.dumps(msgDict))
        
        if len(self._clientList) > self._maxClients:
           self.__dealWithDupes(idToPos) 
    
    '''
    Name: __dealWithDupes
    Parameters: idToPos: dict
    Returns: None
    Purpose: To deal with the potential that there are duplicate
    players internally
    '''
    def __dealWithDupes(self, idToPos: dict) -> None:
        dupeIDs: list[int]|None = self.__findDupeIDs(list(idToPos.keys()))
        if dupeIDs is not None:
            noDeleted: int = 0
            for ID in dupeIDs:
                self._clientList.remove(idToPos[ID]+noDeleted)
                noDeleted += 1
        else:
            raise Exception("Internal Client Handling Error: Dupes Detected when\n there shouldn't be")

    '''
    Name: __findDupeIDs 
    Parameters: IDs:list[int]
    Returns: list[int]|None
    Purpose: To find duplicate playerIDs within the given list
    '''
    def __findDupeIDs(self, IDs:list[int]) -> list[int]|None:
        retVal: list[int] = []
        for ID in IDs:
            noTimes: int = IDs.count(ID)
            if noTimes > 1:
                retVal.append(ID)

        if retVal[0] is None:
            return None
        else:
            return retVal

    '''
    Name: beginGame
    Parameters: None
    Returns: None
    Purpose: Sends each of the clients within the clientList variable the message that the game is beginning,
    and sends them the necessary information required to begin the game
    '''
    def beginGame(self):
        
        self.preStartChecks()

        while self.__waiting != 0:
            pass

        messageDict: dict = {
            "type": "beginGame",
            "data": {
                "platformsPos": self._platformPositions,
                "positionList": None,
                "playerID": None,
                "colourTuple": None,
                "otherPlayersInfo": {}
            }
        }

        msgHolder: dict = messageDict

        # Sends each of the clients the information that they will need to create the stage and all of the opponents
        for client in self._clientList:

            messageDict["data"]["positionList"] = client.getSpawnPoint()
            messageDict["data"]["playerID"] = client.getPlayerID()
            messageDict["data"]["colourTuple"] = client.getPlayerColour()

            for connection in self.__clientList:
                if connection != client:
                    messageDict["data"]["otherPlayersInfo"][connection.getPlayerID()] = {
                        "positionList": connection.getSpawnPoint(),
                        "colourTuple": connection.getPlayerColour(),
                        "playerID": connection.getPlayerID(),
                        "charType": {
                                "caster": connection.getCaster(),
                                "element": connection.getElement()
                            }
                    }

            print(messageDict)
            client.sendData(json.dumps(messageDict))
            messageDict = msgHolder
        self.__beginTime = time.time()
        self.checkForPlatInfo()


    '''
    Name: checkForPlatInfo
    Parameters: None
    Returns: None
    Purpose: After 3s of the game beginning, if 
    the clients still haven't sent over the exact platform
    information, it will call a function that generates an estimate
    '''
    def checkForPlatInfo(self, size: list[int] = [20,500]):
        time.sleep(3)

        for i in range(len(self._platforms)):
            plat = self._platforms[i]
            platPos: list[int] = plat.getPos()
            
            if plat.getTop() is None:
                self._platforms[i].setTop(platPos[1])
            
            if plat.getBottom() is None:
                self._platforms[i].setBottom(platPos[1]+size[0])
            
            if plat.getLeft() is None:
                self._platforms[i].setLeft(platPos[0])
            
            if plat.getRight() is None:
                self._platforms[i].setRight(platPos[0]+size[1])



    '''
    Name: timeCheck
    Parameters: None
    Returns: None
    Purpose: Checks if the time has ran out, and if it has
    runs the timeUp function
    '''
    def timeCheck(self):
        while (time.time()-self.__beginTime) < self.__lengthOfGame:
            pass
        self.__timeUp()

    '''
    Name: getTimeRemaining
    Parameters: None
    Returns: None
    Purpose: Sends clients a message letting them know how long is left
    on the timer
    '''
    def getTimeRemaining(self):
        for client in self._clientList:
            timeRemaining = {
                    "type": "timeLeft",
                    "data": self.__lengthOfGame - (time.time()-self.__beginTime) 
                    }
            client.sendData(json.dumps(timeRemaining).encode())

    '''
    Name: __timeUp
    Parameters: None
    Returns: None
    Purpose: Sends all the clients the message that the game has ended,
    as well as information to see who has won
    '''
    def __timeUp(self):
        pass

    '''
    Name: __missingCaster
    Parameters: conn:object, msgData: str
    Returns: None
    Purpose: To fill out the missing caster
    information given by a client
    '''
    def __missingCaster(self, conn, msgData: str) -> None:
        try:
            clPos: int = self._getClientPosition(conn)
            self._clientList[clPos].setCaster(msgData)
            self._waiting -= 1
        except Exception as e:
            print("PS Missing Caster Error:", e)
            print("Org msgData:", msgData)

    '''
    Name: __missingElement
    Parameters: conn:object, msgData:str
    Returns: None
    Purpose: To fill out the missing element
    information given by a client
    '''
    def __missingElement(self, conn, msgData: str) -> None:
        try:
            clPos: int = self._getClientPosition(conn)
            self._clientList[clPos].setElement(msgData)
            self._waiting -= 1
        except Exception as e:
            print("PS Missing Element Error:", e)
            print("Org msgData:", msgData)

    '''
    Name: __casterInfoFill
    Parameters: conn, msgData: dict
    Returns: None
    Purpose: To fill out a client's caster information
    based upon the info given
    '''    
    def __casterInfoFill(self, conn, msgData: dict) -> None:
        try:
            clPos: int = self.__getClientPosition(conn)
            self.__clientList[clPos].setElement(msgData["element"])
            self.__clientList[clPos].setCaster(msgData["caster"])
        except Exception as e:
            print("casterInfoFill Error:", e)
            print("Org msgData:", msgData)

    '''
    Name: __messageHandling
    Parameters: message:dictionary, conn:object
    Returns: None
    Purpose: Handles what to do with the message received from a client
    '''
    def __messageHandling(self, message:dict, conn) -> None:
        try:
            if message["type"] == "movement":
                self._clientMoved(conn, message["data"])

            if message["type"] == "missingCaster": 
                self.__missingCaster(conn, message["data"])

            if message["type"] == "missingElement":
                self.__missingElement(conn, message["data"])

            if message["type"] == "disconn":
                self._clientDisconn(message["data"])

            if message["type"] == "platformInfo":
                self._platformInfoCreate(message["data"])

            # Since spellcaster information is not automatically filled in, it needs to be set through a seperate message
            if message["type"] == "casterInfo":
               self._casterInfoFill(conn, message["data"])

            if message["type"] == "legalCheck":
                self._legalMove(message["data"])

        except Exception as e:
            print("Error1:", e)
            print("Err1 Org Messsage:", message)
            print("Err1 Type:", type(message))


if __name__ == "__main__":
    pass
