import json
import socket
import threading
import time
from random import choice, randint

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

'''
Name: Client
Purpose: Client class for the private server, to make managing data about 
any given player easier
'''
class Client:
    '''
    Name: __init__
    Parameters: conn:object, spawnPoint:tuple, playerID:integer, size:list
    Returns: None
    Purpose: Constructor to set the initial values
    of the Client object
    '''
    def __init__(self, conn, spawnPoint, playerID, size=[40,40]):
        self.__client = conn
        self.__spawnPoint = spawnPoint
        self.__element = None
        self.__spellCaster = None
        self.__playerID = playerID
        self.__colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.position = list(spawnPoint)
        self.__size = size

    '''
    Name: sendData
    Parameters: msgToSend:dictionary
    Returns: None
    Purpose: Sends data through the connection
    '''
    def sendData(self, msgToSend):
        self.__client.send(msgToSend)

    # Getters and setters

    '''
    Name: setElement
    Parameters: element: object
    Returns: None
    Purpose: Setter for self.__element
    '''
    def setElement(self, element):
        self.__element = element

    '''
    Name: setSpellCaster
    Parameters: spellCaster: object
    Returns: None
    Purpose: Setter for self.__spellCaster
    '''
    def setSpellCaster(self, spellCaster):
        self.__spellCaster = spellCaster

    '''
    Name: getSpawnPoint
    Parameters: None
    Returns: self.__spawnPoint:list
    Purpose: Getter for self.__spawnPoint
    '''
    def getSpawnPoint(self):
        return self.__spawnPoint

    '''
    Name: getSize
    Parameters: None
    Returns: self.__size:list
    Purpose: Getter for self.__size 
    '''
    def getSize(self):
        return self.__size

    '''
    Name: getClient
    Parameters: None
    Returns: self.__client:object
    Purpose: Getter for self.__client
    '''
    def getClient(self):
        return self.__client

    '''
    Name: getPlayerID
    Parameters: None
    Returns: self.__playerID:integer
    Purpose: Getter for self.__playerID
    '''
    def getPlayerID(self):
        return self.__playerID

    '''
    Name: getElement
    Parameters: None
    Returns: self.__element
    Purpose: Getter for self.__element
    '''
    def getElement(self):
        return self.__element

    '''
    Name: getPlayerColour
    Parameters: None
    Returns: self.__colour:tuple
    Purpose: Getter for self.__colour
    '''
    def getPlayerColour(self):
        return self.__colour

    '''
    Name: getCaster
    Parameters: None
    Returns: self.__spellCaster
    Purpose: Getter for self.__spellCaster
    '''
    def getCaster(self):
        return self.__spellCaster

'''
Name: Server
Purpose: Server class to handle connections from the different clients. Different to the public server's
Server class, due to the differences in functionality required from both of them
'''
class Server:
    '''
    Name: __init__
    Parameters: maxClients:integer, lengthOfGame:integer, platformPositions:list
    Returns: None
    Purpose: Constructor to set the initial values
    of the Server object
    '''
    def __init__(self, maxClients, lengthOfGame, platformPositions):
        self.__HOST = socket.gethostbyname(socket.gethostname())
        self.__PORT = 50001
        self.__clientList = []
        self.__maxClients = int(maxClients)
        self.__lengthOfGame = int(lengthOfGame)
        self.__platformPositions = platformPositions
        self.__platforms = []
        self.__spawnPoints = []
        self.password = None
        self.__beginTime = None

    '''
    Name: start
    Parameters: None
    Returns: None
    Purpose: Starts listening for connections from different clients. Will only accept connections
    until it reaches the amount of clients connected as pre-determined on the creation of the object
    '''
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__HOST, self.__PORT))
            s.listen(1)
            print("Server Setup and listening on port", self.__PORT)
            print(self.__maxClients)

            for i in range(len(self.__platformPositions)):
                self.__spawnPoints.append((self.__platformPositions[i][0], self.__platformPositions[i][1]+20))

            for platform in self.__platformPositions:
                self.__platforms.append(Platform(platform))

            # Should only accept new connections while the length of the client lists is less than the max number of connections
            while len(self.__clientList) < self.__maxClients:
                conn, addr = s.accept()
                print("New Connection from ", addr)

                colour = (randint(0, 255), randint(0, 255), randint(0, 255))
                position = choice(self.__spawnPoints)
                # playerIDMessage = json.dumps({"type": "playerID",
                #                               "data": {"playerID": len(self.__clientList) + 1, "colourTuple": colour,
                #                                        "positionList": position}})
                # print(playerIDMessage)
                # conn.send(playerIDMessage.encode())
                time.sleep(0.1)
                self.__clientList.append(Client(conn, choice(self.__spawnPoints),len(self.__clientList) + 1))
                print(len(self.__clientList))
                # Separate function used so that it will still continue running after the while loop in this function stops running
                self.startListening(conn)
                # Once the required number of clients has joined, send the start information to all the clients in '__clientList'
                if len(self.__clientList) >= self.__maxClients:
                    print("Beginning Game!")
                    self.beginGame()
                    break

    '''
    Name: startListening
    Parameters: conn:object
    Returns: None
    Purpose: Creates a thread that will begin listening for messages from the connection passed into
    the function
    '''
    def startListening(self, conn):
            threading.Thread(target=self.recv_from_client, args=(conn,)).start()

    '''
    Name: beginGame
    Parameters: None
    Returns: None
    Purpose: Sends each of the clients within the clientList variable the message that the game is beginning,
    and sends them the necessary information required to begin the game
    '''
    def beginGame(self):
        messageDict = {
            "type": "beginGame",
            "data": {
                "platformsPos": self.__platformPositions,
                "positionList": None,
                "playerID": None,
                "colourTuple": None,
                "otherPlayersInfo": {}
            }
        }

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

            # print(messageDict)
            client.sendData(json.dumps(messageDict).encode())
            messageDict = {
                "type": "beginGame",
                "data": {
                    "platformsPos": self.__platformPositions,
                    "positionList": None,
                    "playerID": None,
                    "colourTuple": None,
                    "otherPlayersInfo": {}
                }
            }
        self.__beginTime = time.time()
    
    def timeCheck(self):
        while (time.time()-self.__beginTime) < self.__lengthOfGame:
            pass
        self.__timeUp()


    def getTimeRemaining(self):
        for client in self.__clientList:
            timeRemaining = {
                    "type": "timeLeft",
                    "data": self.__lengthOfGame - (time.time()-self.__beginTime) 
                    }
            client.sendData(json.dumps(timeRemaining).encode())

    def __timeUp(self):
        pass

    '''
    Name: messageHandling
    Parameters: message:dictionary, conn:object
    Returns: None
    Purpose: Handles what to do with the message received from a client
    '''
    def __messageHandling(self, message, conn):
        try:
            if message["type"] == "movement":
                for client in self.__clientList:
                    if client.getClient() == conn:
                        clPos = client.getPlayerID - 1

                self.__clientList[clPos].position[0], self.__clientList[clPos].position[1] = message["data"]["posX"], message["data"]["posY"]

            if message["type"] == "disconn":
                self.tellClientsOfDisconn(message["data"]["playerID"] - 1)
                self.__clientList[message["data"]["playerID"] - 1].client.close()
                self.__clientList.pop(message["data"]["playerID"] - 1)
                print("player disconnected")

            if message["type"] == "platformInfo":
                print("CREATING PLATFORM INFORMATION")
                iterator = 0
                for platform in message["data"]:
                    self.__platforms[iterator].setTop(platform["platformTop"])
                    self.__platforms[iterator].setBottom(platform["platformBottom"])
                    self.__platforms[iterator].setLeft(platform["platformLeft"])
                    self.__platforms[iterator].setRight(platform["platformRight"])
                    print("PLATFORM INFO RECORDED")
                    p = self.__platforms[iterator]
                    print([p.getTop(), p.getBottom(), p.getLeft(), p.getRight()])
                    iterator += 1

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
            print("Error:", e)

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
                    message = dict(json.loads(data.decode()))
                    if message["type"] == "movement":
                        for client in self.__clientList:
                            if client.getClient() == conn:
                                clPos = client.getPlayerID() - 1

                        self.__clientList[clPos].position[0], self.__clientList[clPos].position[1] = message["data"][
                            "posX"], message["data"]["posY"]

                    if message["type"] == "disconn":
                        self.tellClientsOfDisconn(message["data"]["playerID"] - 1)
                        self.__clientList[message["data"]["playerID"] - 1].client.close()
                        self.__clientList.pop(message["data"]["playerID"] - 1)
                        print("player disconnected")

                    if message["type"] == "platformInfo":
                        print("CREATING PLATFORM INFORMATION")
                        iterator = 0
                        for platform in message["data"]:
                            self.__platforms[iterator].setTop(platform["platformTop"])
                            self.__platforms[iterator].setBottom(platform["platformBottom"])
                            self.__platforms[iterator].setLeft(platform["platformLeft"])
                            self.__platforms[iterator].setRight(platform["platformRight"])
                            print("PLATFORM INFO RECORDED")
                            p = self.__platforms[iterator]
                            print([p.getTop(), p.getBottom(), p.getLeft(), p.getRight()])
                            iterator += 1

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
                except Exception as err:
                    print(data.decode())
                    print("Error:", err)

                finally:
                    try:
                        for client in self.__clientList:
                            if client is not None and client.getClient() != conn and (
                                    message["type"] != "platformInfo" or message["type"] != "legalCheck"):
                                client.sendData(data)
                    except Exception as e:
                        print("Error:", e)

if __name__ == "__main__":
    pass
