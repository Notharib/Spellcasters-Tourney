import json

from random import randint, choice

from serverFunctions import generatePlatforms, generateSpawnPoints
from characterCreation import BaseCharacter
from gameLogic import data_handling


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
    def __init__(self, maxClients = 10, host="127.0.0.1", port=50000) -> None:
        self._HOST: str = host
        self._PORT: int = port
        self._clientList: list = []
        self._maxClients: int = int(maxClients)
        self._platformPositions: list[int] = [[randint(0,800),randint(0,800)] for i in range(3)]
        print("Created Platforms Positions @", self._platformPositions)
        self._platforms: list = generatePlatforms(self._platformPositions)
        self._spawnPoints: list = generateSpawnPoints(self._platformPositions)

    def start(self) -> None:
        pass

    '''
    Name: _getClientPosition
    Parameters: conn:object
    Returns: int
    Purpose: Gets the position of a certain client object within the clientList variable
    '''
    def _getClientPosition(self, conn) -> int:
        for client  in self._clientList:
            if client.getClient() == conn:
                return client.getPlayerID() - 1

    '''
    Name: _clientMoved 
    Parameters: conn:object, msgData: dict
    Returns: None
    Purpose: To handle what the server should do when
    a player moves
    '''
    def _clientMoved(self, conn, msgData: dict) -> None:
        try:
            clPos: int = self._getClientPosition(conn)
            self._clientList[clPos].setPosition([msgData["posX"], msgData["posY"]])
        except Exception as e:
            print("Client Move Error:", e)
            print("Org msgData:", msgData)

    
    '''
    Name: _clientDisconn 
    Parameters: msgData: dict
    Returns: None
    Purpose: To handle what should happen when the server recieves the
    message that a client has disconnected from the server
    '''    
    def _clientDisconn(self, msgData: dict) -> None:
        try:
            self.tellClientsOfDisconn(msgData["playerID"]-1)
            self._clientList[msgData["playerID"] - 1].getClient().close()
            self._clientList.pop(msgData["playerID"] - 1)
            print("Player Disconnected")
        except Exception as e:
            print("Client Disconnection Error:", e)
            print("Org msgData:", msgData)

    '''
    Name: __platformInfoCreate
    Parameters: msgData:list[dict]
    Returns: None
    Purpose: Creates internal platform objects
    based off of the information given by the client
    '''    
    def _platformInfoCreate(self, msgData: list[dict]) -> None:
        try:
            print("CREATING PLATFORM INFORMATION")
            iterator = 0
            for platform in msgData:
                self._platforms[iterator].setTop(platform["platformTop"])
                self._platforms[iterator].setBottom(platform["platformBottom"])
                self._platforms[iterator].setLeft(platform["platformLeft"])
                self._platforms[iterator].setRight(platform["platformRight"])
                print("PLATFORM INFO RECORDED")
                p = self._platforms[iterator]
                print([p.getTop(), p.getBottom(), p.getLeft(), p.getRight()])
                iterator += 1
        except Exception as e:
            print("platformInfoCreate Error:",e)
            print("Org msgData:", msgData)

    '''
    Name: _casterInfoFill
    Parameters: conn, msgData: dict
    Returns: None
    Purpose: To fill out a client's caster information
    based upon the info given
    '''    
    def _casterInfoFill(self, conn, msgData: dict) -> None:
        try:
            clPos: int = self._getClientPosition(conn)
            self._clientList[clPos].setElement(msgData["element"])
            self._clientList[clPos].setCaster(msgData["caster"])
        except Exception as e:
            print("casterInfoFill Error:", e)
            print("Org msgData:", msgData)

    '''
    Name: _legalMove 
    Parameters: msgData:dict
    Returns: None
    Purpose: To determine whether a move that a client is about to
    make would be legal
    '''    
    def _legalMove(self, msgData: dict) -> None:
        try:
            clientMove = self._clientList[msgData["playerID"] - 1]

            clientCPos: list[int] = [clientMove.getX(), clientMove.getY()] 

            closestPlat = None
            for platform in self._platforms:
                if closestPlat is None:
                    closestPlat = platform
                else:
                    #print("PlatCheck:", platform.getTop())
                    if msgData["direction"] == "y":
                        if (platform.getTop() >= clientCPos[1] - msgData["amount"] or platform.getTop() <= clientCPos[1] - msgData["amount"]) and closestPlat.getTop() - platform.getTop() < 0:
                            closestPlat = platform
                        else:
                            if (platform.getTop() >= clientCPos[0] - msgData["amount"] or platform.getTop() <= clientCPos[0] - msgData["amount"]) and closestPlat.getTop() - platform.getTop() < 0:
                                closestPlat = platform

            if closestPlat is not None:
                if msgData["direction"] == "y":
                    if clientCPos[1] - msgData["amount"] <= closestPlat.getPos()[1] + closestPlat.getSize()[0]:                            
                        clientMove.sendData(json.dumps({"type": "MOVENOTLEGAL"}))
                    else:
                        clientMove.sendData(json.dumps({"type": "MOVELEGAL"}))
                else:
                    if clientCPos[0] - msgData["amount"] + clientCPos[0] == closestPlat.getPos()[0] or clientCPos[0] - msgData["amount"] <= closestPlat.getPos()[0] + closestPlat.getSize()[1]:
                        clientMove.sendData(json.dumps({"type": "MOVENOTLEGAL"}))                        
                    else:
                        clientMove.sendData(json.dumps({"type": "MOVELEGAL"}))
        except Exception as e:
            print("LegalMove Error",e)
            print("Org msgData:", msgData)


    '''
    Name: _messageHandling
    Parameters: message:dictionary, conn:object
    Returns: None
    Purpose: Handles what to do with the message received from a client
    '''
    def _messageHandling(self, message:dict, conn) -> None:
        try:
            if message["type"] == "movement":
                self._clientMoved(conn, message["data"])

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
                                self._messageHandling(message=msg, conn=conn)

                except Exception as err:
                    print(data.decode())
                    print("Error2:", err)

                finally:
                    try:
                        if msgList is not None:
                            for message in msgList:
                                for client in self._clientList:
                                    if client is not None and client.getClient() != conn and (
                                            message["type"] != "platformInfo" or message["type"] != "legalCheck"):
                                        client.sendData(data.decode())
                    except Exception as e:
                        print("Error3:", e)
                        print("Err3 Org Decode:", data.decode())

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
Purpose: Client Class to handle how the Private Server should deal with
players/connections
'''
class Client(BaseCharacter):
    '''
    Name: __init__
    Parameters: conn:object, position:list[int], playerID:int, colour:tuple[int,int,int]
    Returns: None
    Purpose: Constructor to set the initial values
    of the Client object
    '''
    def __init__(self, conn, position: list[int], playerID: int, colour: tuple[int,int,int]) -> None:
        super().__init__()
        self.__conn = conn
        self.__X: int = position[0]
        self.__Y: int = position[1]
        self.__playerID: int = playerID
        self.__colour: tuple[int,int,int] = colour

    '''
    Name: sendData
    Parameters: message:str
    Returns: None
    Purpose: Sends data to the client
    '''
    def sendData(self, message: str) -> None:
        self.__conn.send(message.encode())

    '''
    Name: getClient
    Parameters: None
    Returns: self.__conn
    Purpose: Getter for the client's connection
    '''
    def getClient(self) -> any:
        return self.__conn

    '''
    Name: getX
    Parameters: None
    Returns: self.__X:int
    Purpose: Getter for the client's X
    coordinate
    '''
    def getX(self) -> int:
        return self.__X
    
    '''
    Name: getY
    Parameters: None
    Returns: self.__Y: int
    Purpose: Getter for the client's Y
    coordinate
    '''
    def getY(self) -> int:
        return self.__Y

    '''
    Name: getPlayerID
    Parameters: None
    Returns: self.__playerID:int
    Purpose: Getter for the client's
    playerID
    '''
    def getPlayerID(self) -> int:
        return self.__playerID

    '''
    Name: getSpawnPoint
    Parameters: None
    Returns: list[int]
    Purpose: Getter for the client's
    initial position
    '''
    def getSpawnPoint(self) -> list[int]:
        return [self.__X, self.__Y]

    '''
    Name: getPlayerColour
    Parameters: None
    Returns: self.__colour:tuple[int,int,int]
    Purpose: Getter for the client's
    colour
    '''
    def getPlayerColour(self) -> tuple[int,int,int]:
        return self.__colour

    '''
    Name: getCaster
    Parameters: None
    Returns: self.__Caster:str
    Purpose: Getter for the client's
    caster
    '''
    def getCaster(self) -> str:
        return self._Caster

    '''
    Name: getElement
    Parameters: None
    Returns: self._Element:str
    Purpose: Getter for the client's
    element
    '''
    def getElement(self) -> str:
        return self._Element

    '''
    Name: setPosition
    Parameters: position:list[int]
    Returns: None
    Purpose: Setter for the client's position
    '''
    def setPosition(self, position:list[int]) -> None:
        self.__X = position[0]
        self.__Y = position[1]

    '''
    Name: setHP
    Parameters: HP:int
    Returns: None
    Purpose: Setter for the client's HP
    '''
    def setHP(self, HP:int) -> None:
        self._HP = HP

    '''
    Name: setElement
    Parameters: element:str
    Returns: None
    Purpose: Setter for the client's Element
    '''
    def setElement(self, element:str) -> None:
        self._Element = element

    '''
    Name: setHP
    Parameters: caster:str
    Returns: None
    Purpose: Setter for the client's Caster
    '''
    def setCaster(self, caster: str) -> None:
        self._Caster = caster
