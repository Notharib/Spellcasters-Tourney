import json
import socket
import threading
import time
from random import choice, randint

from gameLogic import data_handling
from characterCreation import BaseCharacter

class Client(BaseCharacter):

    def __init__(self, conn, position, playerNo) -> None:
        super().__init__()
        self.__conn = conn

    def getConn(self) -> any:
        return self.__conn

'''
Name: Server
Purpose: Server class to handle connections from the different clients. Different to the public server's
Server class, due to the differences in functionality required from both of them
'''
class Server:
    '''
    Name: __init__
    Parameters: maxClients:integer, lengthOfGame:integer
    Returns: None
    Purpose: Constructor to set the initial values
    of the Server object
    '''
    def __init__(self, maxClients:int, lengthOfGame:int) -> None:
        self.__HOST: str = socket.gethostbyname(socket.gethostname())
        self.__PORT: int = 50001
        self.__clientList: list = []
        self.__maxClients: int = int(maxClients)
        self.__lengthOfGame: int = int(lengthOfGame)
        self.__platformPositions: list[int] = [[randint(0,800),randint(0,800)] for i in range(3)]
        print("Created Platforms Positions @", self.__platformPositions)
        self.__platforms: list = generatePlatforms(self.__platformPositions)
        self.__spawnPoints: list = []
        self.password: None|str = None
        self.__beginTime: None|int|float = None

    '''
    Name: start
    Parameters: None
    Returns: None
    Purpose: Starts listening for connections from different clients. Will only accept connections
    until it reaches the amount of clients connected as pre-determined on the creation of the object
    '''
    def start(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__HOST, self.__PORT))
            s.listen(1)
            print("Server Setup and listening on port", self.__PORT)
            print(self.__maxClients)

            for i in range(len(self.__platformPositions)):
                self.__spawnPoints.append((self.__platformPositions[i][0], self.__platformPositions[i][1]+20))

            # Should only accept new connections while the length of the client lists is less than the max number of connections
            while len(self.__clientList) < self.__maxClients:
                conn, addr = s.accept()
                print("New Connection from ", addr)

                colour = (randint(0, 255), randint(0, 255), randint(0, 255))
                position = choice(self.__spawnPoints)

                time.sleep(0.1)
                self.__clientList.append(Client(conn, choice(self.__spawnPoints),len(self.__clientList) + 1))
                print(len(self.__clientList))
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
    Name: beginGame
    Parameters: None
    Returns: None
    Purpose: Sends each of the clients within the clientList variable the message that the game is beginning,
    and sends them the necessary information required to begin the game
    '''
    def beginGame(self):
        messageDict: dict = {
            "type": "beginGame",
            "data": {
                "platformsPos": self.__platformPositions,
                "positionList": None,
                "playerID": None,
                "colourTuple": None,
                "otherPlayersInfo": {}
            }
        }

        msgHolder: dict = messageDict

        # Sends each of the clients the information that they will need to create the stage and all of the opponents
        for client in self.__clientList:

            messageDict["data"]["positionList"] = client.getSpawnPoint()
            messageDict["data"]["playerID"] = client.getPlayerID()
            messageDict["data"]["colourTuple"] = client.getPlayerColour()

            for connection in self.__clientList:
                if connection != client:
                    messageDict["data"]["otherPlayersInfo"][connection.getPlayerID()] = {
                        "type": connection.getCaster(),
                        "element": connection.getElement(),
                        "positionList": connection.getSpawnPoint(),
                        "colourTuple": connection.getPlayerColour(),
                        "playerID": connection.getPlayerID()
                    }

            print(messageDict)
            client.sendData(json.dumps(messageDict).encode())
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

        for i in range(len(self.__platforms)):
            plat = self.platforms[i]
            platPos: list[int] = plat.getPos()
            
            if plat.getTop() is None:
                self.__platforms[i].setTop(platPos[1])
            
            if plat.getBottom() is None:
                self.__platforms[i].setBottom(platPos[1]+size[0])
            
            if plat.getLeft() is None:
                self.__platforms[i].setLeft(platPos[0])
            
            if plat.getRight() is None:
                self.__platforms[i].setRight(platPos[0]+size[1])



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
        for client in self.__clientList:
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
    Name: __getClientPosition
    Parameters: conn:object
    Returns: int
    Purpose: Gets the position of a certain client object within the clientList variable
    '''
    def __getClientPosition(self, conn) -> int:
        for client  in self.__clientList:
            if client.getClient() == conn:
                return client.getPlayerID() - 1

    '''
    Name: messageHandling
    Parameters: message:dictionary, conn:object
    Returns: None
    Purpose: Handles what to do with the message received from a client
    '''
    def __messageHandling(self, message:dict, conn) -> None:
        try:
            if message["type"] == "movement":
                clPos: int = self.__getClientPosition(conn)

                self.__clientList[clPos].position[0], self.__clientList[clPos].position[1] = message["data"]["posX"], message["data"]["posY"]

            if message["type"] == "disconn":
                self.tellClientsOfDisconn(message["data"]["playerID"] - 1)
                self.__clientList[message["data"]["playerID"] - 1].client.close()
                self.__clientList.pop(message["data"]["playerID"] - 1)
                print("player disconnected")

#            if message["type"] == "platformInfo":
#                print("CREATING PLATFORM INFORMATION")
#                iterator = 0
#                for platform in message["data"]:
#                    self.__platforms[iterator].setTop(platform["platformTop"])
#                    self.__platforms[iterator].setBottom(platform["platformBottom"])
#                    self.__platforms[iterator].setLeft(platform["platformLeft"])
#                    self.__platforms[iterator].setRight(platform["platformRight"])
#                    print("PLATFORM INFO RECORDED")
#                    p = self.__platforms[iterator]
#                    print([p.getTop(), p.getBottom(), p.getLeft(), p.getRight()])
#                    iterator += 1

            # Since spellcaster information is not automatically filled in, it needs to be set through a seperate message
            if message["type"] == "casterInfo":
                data = message["data"]
                clPos: int = self.__getClientPosition(conn)

                self.__clientList[clPos].setElement(data["element"])
                self.__clientList[clPos].setCaster(data["caster"])

            if message["type"] == "legalCheck":
                messageData = message["data"]
                print("LEGALMOVECHECK")
                print(messageData)
                clientMove = self.__clientList[messageData["playerID"] - 1]
                closestPlat = None
                for platform in self.__platforms:
                    if closestPlat is None:
                        closestPlat = platform
                    else:
                        print("NonePlatCheck:", platform.getTop())
                        if messageData["direction"] == "y":
                            if (platform.getTop() >= clientMove.position[1] - messageData[
                                "amount"] or platform.getTop() <= clientMove.position[1] - messageData[
                                    "amount"]) and closestPlat.getTop() - platform.getTop() < 0:
                                closestPlat = platform
                        else:
                            if (platform.getTop() >= clientMove.position[0] - messageData[
                                "amount"] or platform.getTop() <= clientMove.position[0] - messageData[
                                    "amount"]) and closestPlat.getTop() - platform.getTop() < 0:
                                closestPlat = platform

                if closestPlat is not None:
                    if messageData["direction"] == "y":
                        if clientMove.position[1] - messageData["amount"] <= closestPlat.getPos()[1] + \
                                closestPlat.getSize()[0]:
                            clientMove.sendData(json.dumps({"type": "MOVENOTLEGAL"}).encode())
                        else:
                            clientMove.sendData(json.dumps({"type": "MOVELEGAL"}).encode())
                    else:
                        if clientMove.position[0] - messageData["amount"] + clientMove.getSize()[0] == \
                                closestPlat.getPos()[0] or clientMove.position[0] - messageData["amount"] <= \
                                closestPlat.getPos()[0] + closestPlat.getSize()[1]:
                            clientMove.sendData(json.dumps({"type": "MOVENOTLEGAL"}).encode())
                        else:
                            clientMove.sendData(json.dumps({"type": "MOVELEGAL"}).encode())
        except Exception as e:
            print("Error1:", e)

    '''
    Name: recv_from_client
    Parameters: conn:object
    Returns: None
    Purpose: Listens for a message from the client, and handles what to do with it
    '''
    def recv_from_client(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                try:
                    if data.decode() is not None:
                        msgList: list[dict] = data_handling(data.decode())
                        if msgList is not None:
                            for msg in msgList:
                                self.__messageHandling(message=msg, conn=conn)

                except Exception as err:
                    print(data.decode())
                    print("Error2:", err)

                finally:
                    try:
                        if msgList is not None:
                            for message in msgList:
                                for client in self.__clientList:
                                    if client is not None and client.getClient() != conn and (
                                            message["type"] != "platformInfo" or message["type"] != "legalCheck"):
                                        client.sendData(data)
                    except Exception as e:
                        print("Error3:", e)

if __name__ == "__main__":
    pass
