import socket
import json
import threading
import random
import time
import requests

from gameLogic import data_handling
from logger import addToLog, generateLogFile
from arenaHandling import platformGenerate

"""
Name: Client
Purpose: Client class for the private server, to make managing data about 
any given player easier
"""


class Client:
    """
    Name: __init__
    Parameters: position:list, colour:tuple, cl:object, playerID:integer, address:string, size:list
    Returns: None
    Purpose: Constructor to set the initial values
    of the Client object
    """

    def __init__(self, position, colour, cl, playerID, address, size=[40, 40]):
        self.addr = address
        self.client = cl
        self.position = position
        self.colour = colour
        self.playerID = playerID
        self.size = size

    """
    Name: sendData
    Parameters: msg:dict
    Returns: None
    Purpose: Sends data to the client
    """

    def sendData(self, msg: dict) -> None:
        self.client.send(json.dumps(msg).encode())


"""
Name: Platform
Purpose: To have platforms that players are able to move around on
"""


class Platform:
    """
    Name: __init__
    Parameters: position:list, platformId: integer, colour:tuple, platformSize:list
    Returns: None
    Purpose: Constructor to set the initial values
    of the Platform object
    """

    def __init__(
        self,
        position: list[int],
        platformNo: int,
        colour: tuple[int, int, int] = (0, 255, 0),
        platformSize: list[int] = [20, 500],
    ):
        self.__position: list[int] = position
        self.__colour: tuple[int, int, int] = colour
        self.__platformSize: list[int] = platformSize
        self.__platformNo: int = platformNo
        self.__spawnPoint: list[int] = self.__generateSpawnPoint()

        self.__top: None | int = None
        self.__bottom: None | int = None
        self.__left: None | int = None
        self.__right: None | int = None

    """
    Name: getPosition
    Parameters: None
    Returns: self.__position: list[int]
    Purpose: Getter for position variable
    """

    def getPosition(self) -> list[int]:
        return self.__position

    """
    Name: getSize
    Parameters: None
    Returns: self.__platformSize: list[int]
    Purpose: Getter for size variable
    """

    def getSize(self) -> list[int]:
        return self.__platformSize

    """
    Name: getPlatformNo
    Parameters: None
    Returns: self.__platformNo:int
    Purpose: Getter for platformNo variable
    """

    def getPlatformNo(self) -> int:
        return self.__platformNo

    """
    Name: getTop
    Parameters: None
    Returns: self.__top
    Purpose: Getter for top variable
    """

    def getTop(self) -> None | int:
        return self.__top

    """
    Name: getBottom
    Parameters: None
    Returns: self.__
    Purpose: Getter for bottom variable
    """

    def getBottom(self) -> None | int:
        return self.__bottom

    """
    Name: getLeft
    Parameters: None
    Returns: self.__left
    Purpose: Getter for left variable
    """

    def getLeft(self) -> None | int:
        return self.___left

    """
    Name: getRight
    Parameters: None
    Returns: self.__right
    Purpose: Getter for right variable
    """

    def getRight(self) -> None | int:
        return self.__right

    """
    Name: setTop
    Parameters: top:int
    Returns: None
    Purpose: Setter for top variable
    """

    def setTop(self, top: int) -> None:
        self.__top = top

    """
    Name: setBottom
    Parameters: bottom:int 
    Returns: None
    Purpose: Setter for bottom variable
    """

    def setBottom(self, bottom: int) -> None:
        self.__bottom = bottom

    """
    Name: setLeft
    Parameters: left:int
    Returns: None
    Purpose: Setter for left variable
    """

    def setLeft(self, left: int) -> None:
        self.__left = left

    """
    Name: setRight
    Parameters: right: int
    Returns: None
    Purpose: Setter for right variable
    """

    def setRight(self, right: int) -> None:
        self.__right = right

    """
    Name: generateSpawnPoint
    Parameters: playerSize: int
    Returns: list[int]
    Purpose: Generates a player's spawn point based
    for this platform
    """

    def __generateSpawnPoint(self, playerSize: int = 40) -> list[int]:
        X: int = self.position[0] + self.platformSize[0] // 2
        Y: int = self.position[1] - (playerSize + playerSize // 2)

        return [X, Y]

    """
    Name: getSpawnPoint
    Parameters: None
    Returns: self.__spawnPoint: list[int]
    Purpose: Getter for the platform's spawn point
    """

    def getSpawnPoint(self) -> list[int]:
        return self.__spawnPoint


"""
Name: Server
Purpose: Server class to handle connections from the different clients. Different to the private server's
Server class, due to the differences in functionality required from both of them
"""


class Server:
    """
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Server object
    """

    def __init__(self, logPath: str) -> None:
        self.__logPath: str = logPath
        self.__HOST: str = "127.0.0.1"
        self.__PORT: int = 50000
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__clientList: list = []
        self.__platformSize: list[int] = [20, 500]
        self.__platforms: list = []
        self.__generateArena(2)
        self.__leaderboard: dict = {}

    """
    Name: generateArena
    Parameters: amountOfPlatforms: int
    Returns: None
    Purpose: Generates all the platforms that the server needs
    """

    def __generateArena(self, amountOfPlatforms: int) -> None:
        platforms: list[list[int]] = platformGenerate(
            amountOfPlatforms, self.__platformSize
        )

        i: int = 0
        for platform in platforms:
            self.__platforms.append(Platform(platform, i))
            i += 1
        addToLog(self.__logPath, "sergeneratearena", extraInfo="GENERATED PLATFORMS")

    def start(self) -> None:
        """
        Name: start
        Parameters: None
        Returns: None
        Purpose: Starts listening for new connections from clients, and handles what to do with them upon joining
        """
        with self.__socket as s:
            s.bind((self.__HOST, self.__PORT))
            s.listen(1)
            print("Server Setup and listening on port", self.__PORT)
            self.__online = True
            while True:
                self.__acceptConnections(s)

    """
    Name: acceptConnections
    Parameters: None
    Returns: None
    Purpose: Accepts new connections to the server
    """

    def __acceptConnections(self, s) -> None:
        conn, addr = s.accept()
        print("New Connection from ", addr)

        # Genreates the information that the client initially needs
        colour: tuple[int, int, int] = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        position: list[int] = random.choice(self.__platforms).getSpawnPoint()

        # Sends the client the information they will initially need so that they can join the server properly
        self.__sendConnInitialInfo(conn, colour, position)

        # Checks if the server is now full (aka reached 10 active players)
        self.__clientList.append(
            Client(position, colour, conn, len(self.__clientList) + 1, addr)
        )
        self.checkIfFull()

        self.__leaderboard[len(self.__clientList) + 1] = 0
        time.sleep(0.1)
        self.notifyClientsOfConn(conn, colour, position)
        threading.Thread(target=self.recv_from_client, args=(conn,)).start()

    def closeConn(self) -> None:
        """
        Name: closeConn
        Parameters: None
        Returns: None
        Purpose: Shuts down the server
        """
        self.__socket.close()

    """
    Name: sendConnInitialInfo
    Parameters: conn: socket, colour: tuple
    Returns: None
    Purpose: Sends the connection the initial info that
    it needs to join the server
    """

    def __sendConnInitialInfo(
        self, conn, colour: tuple[int, int, int], position: list[int]
    ) -> None:
        initialInfoDict: dict = {
            "type": "playerID",
            "data": {
                "playerID": len(self.__clientList) + 1,
                "colourTuple": colour,
                "positionList": position,
            },
        }

        playerIDMessage: str = json.dumps(initialInfoDict)
        print(playerIDMessage)
        conn.send(playerIDMessage.encode())
        time.sleep(0.1)
        self.__createStage(conn)

        if len(self.__clientList) != 0:
            self.createAlreadyJoinedPlayers(conn)

    """
    Name: notifyClientsOfConn
    Parameters: connection:object, colour:tuple, position:list
    Returns: None
    Purpose: Lets all clients in the self.__clientList variable know that a new client has joined, 
    as well as sending them the character data required for the character to be created
    """

    def notifyClientsOfConn(
        self, connection, colour: tuple[int, int, int], position: list
    ) -> None:
        for client in self.__clientList:
            if client.client != connection:
                msgDict: dict = {
                    "type": "playerJoin",
                    "data": {
                        "playerID": len(self.__clientList) + 1,
                        "colourTuple": colour,
                        "positionList": position,
                    },
                }

                message = json.dumps(msgDict)
                client.client.send(message.encode())

    """
    Name: createAlreadyJoinedPlayers
    Parameters: connection:object
    Returns: None
    Purpose: Sends the newly joined player all the clients' information to ensure that they are not out of sync
    """

    def createAlreadyJoinedPlayers(self, connection) -> None:
        for client in self.__clientList:
            msgDict: dict = {
                "type": "playerJoin",
                "data": {
                    "playerID": client.playerID,
                    "colourTuple": client.colour,
                    "positionList": client.position,
                },
            }

            message = json.dumps(msgDict)
            connection.send(message.encode())
            time.sleep(0.2)

    """
    Name: createStage
    Parameters: connection:object
    Returns: None
    Purpose: Sends all the platform information to the newly joined client
    """

    def __createStage(self, connection) -> None:
        for platform in self.__platforms:
            posMsgDic: dict = {
                "type": "createPlat",
                "data": {
                    "position": platform.getPosition(),
                    "size": platform.getSize(),
                    "platformNo": platform.getPlatformNo(),
                },
            }
            positionMessage = json.dumps(posMsgDic)
            connection.send(positionMessage.encode())
            time.sleep(0.2)

    """
    Name: tellClientsOfDisconn
    Parameters: clientToDisconn
    Returns: None
    Purpose: Lets all clients in the self.__clientList variable know that a client has disconnected, and that
    they need to remove that client from their sprite group in order to stay in sync. Also lets the API know that the
    server isn't full
    """

    def tellClientsOfDisconn(self, clientToDisconn: int) -> None:
        requests.post(url="http://127.0.0.1:5000/serverFull", json={"fullValue": "0"})
        for client in self.__clientList:
            if client != self.__clientList[clientToDisconn] and client is not None:
                messageDict = {"type": "disconn", "data": {"playerID": clientToDisconn}}
                client.client.send(json.dumps(messageDict).encode())

    def __kickBrokenPlayer(self, conn) -> None:
        """
        Name: __kickBrokenPlayer
        Parameters: conn
        Returns: None
        Purpose: Kicks broken players from the server,
        and tells the other clients that it is broken so they also
        remove it
        """
        for i in range(len(self.__clientList)):
            if self.__clientList[i].client == conn:
                broPl: int = i

        brokenPlayerID: int = self.__clientList[broPl].playerID

        self.__clientList.pop(broPl)

        msg: dict = {"type": "brokenPlayer", "data": brokenPlayerID}

        for client in self.__clientList:
            client.sendData(msg)

    """
    Name: checkIfFull
    Parameters: None
    Returns: None
    Purpose: Checks if the server is at max capacity (10 active connections), 
    and then if it is, letting the API know that it is full so it 
    shouldn't let any more players join
    """

    def checkIfFull(self) -> None:
        if len(self.__clientList) == 10:
            requests.post(
                url="http://127.0.0.1:5000/serverFull", json={"fullValue": "1"}
            )

    """
    Name: leaderUpd
    Parameters: None
    Returns: None
    Purpose: Sends a POST request to the API to update the information on the public leaderboard
    """

    def leaderUpd(self, playerID: int) -> None:
        requests.post(
            url="http://127.0.0.1:5000/publicLeaderUpd", json={"playerID": playerID}
        )

    """
    Name: recv_from_client
    Parameters: conn:object
    Returns: None
    Purpose: Listens for data being sent by the connection, 
    and then if data is sent, handles what to do with it
    """

    def recv_from_client(self, conn) -> None:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                try:
                    messages = data_handling(data.decode(), self.__logPath)
                    while not messages.is_empty():
                        message = messages.dequeue()
                        if message is not None:
                            self.__messageHandling(message, conn)

                            self.__updClients(conn, message["type"], data)

                except json.JSONDecodeError as err:
                    print(data.decode())
                    print("JSON Syntax Error:", err)
                    addToLog(self.__logPath, "serverRecv", err)

                except ConnectionError as e:
                    print("Server Conn Error", e)
                    self.__kickBrokenPlayer(conn)
                    addToLog(self.__logPath, "serverRecv", e)
                    break

    def __messageHandling(self, message: dict, conn) -> None:
        """
        Name: __messageHandling
        Parameters: message: dict
        Returns:None
        Purpose: Handles messages
        """
        try:
            if message["type"] == "leaderUpd":
                self.leaderUpd(message["data"]["playerID"])

            if message["type"] == "movement":
                self.__playerMoved(message["data"], conn)

            if message["type"] == "disconn":
                self.tellClientsOfDisconn(message["data"]["playerID"] - 1)
                self.__clientList[message["data"]["playerID"] - 1].client.close()
                self.__clientList.pop(message["data"]["playerID"] - 1)

            if message["type"] == "platformInfo":
                self.__platformCreate(message["data"])

            if message["type"] == "legalCheck":
                self.__legalCheck(message["data"])

        except Exception as e:
            addToLog(self.__logPath, "servermsghandling", e)

    def __platformCreate(self, msgData: list) -> None:
        """
        Name: __platformCreate
        Parameters: msgData: lists
        Returns: None
        Purpose:To handle how to create new platforms
        """
        iterator = 0
        for platform in msgData:
            self.__platforms[iterator].setTop(platform["platformTop"])
            self.__platforms[iterator].setBottom(platform["platformBottom"])
            self.__platforms[iterator].setLeft(platform["platformLeft"])
            self.__platforms[iterator].setRight(platform["platformRight"])
            iterator += 1

    def __legalCheck(self, msgData: dict) -> None:
        """
        Name: __legalCheck
        Parameters: msgData: dict
        Returns: None
        Purpose: To check if a move the player just made
        is legal
        """
        clientMove = self.__clientList[msgData["playerID"] - 1]
        closestPlat = None
        for platform in self.__platforms:
            if closestPlat is None:
                closestPlat = platform
            else:
                if msgData["direction"] == "y":
                    if (
                        platform.getTop() >= clientMove.position[1] - msgData["amount"]
                        or platform.getTop()
                        <= clientMove.position[1] - msgData["amount"]
                    ) and closestPlat.getTop() - platform.getTop() < 0:
                        closestPlat = platform
                else:
                    if (
                        platform.getTop() >= clientMove.position[0] - msgData["amount"]
                        or platform.getTop()
                        <= clientMove.position[0] - msgData["amount"]
                    ) and closestPlat.getTop() - platform.getTop() < 0:
                        closestPlat = platform

        if closestPlat is not None:
            if msgData["direction"] == "y":
                if (
                    clientMove.position[1] - msgData["amount"]
                    <= closestPlat.getPosition()[1] + closestPlat.getSize()[0]
                ):
                    clientMove.sendData({"type": "MOVENOTLEGAL"})
                else:
                    clientMove.sendData({"type": "MOVELEGAL"})
            else:
                if (
                    clientMove.position[0] - msgData["amount"] + clientMove.size[0]
                    == closestPlat.getPosition()[0]
                    or clientMove.position[0] - msgData["amount"]
                    <= closestPlat.getPosition()[0] + closestPlat.getSize()[1]
                ):
                    clientMove.sendData({"type": "MOVENOTLEGAL"})
                else:
                    clientMove.sendData({"type": "MOVELEGAL"})

    def __playerMoved(self, msgData: dict, conn) -> None:
        """
        Name: __playerMoved
        Parameters: msgData:dict
        Returns: None
        Purpose:Handles what to do if a player moves
        """
        for client in self.__clientList:
            if client.client == conn:
                clPos = client.playerID - 1

        if msgData["direction"] == "y":
            self.__clientList[clPos].position[1] = msgData["movedTo"]
            # print("changed player position")
        else:
            self.__clientList[clPos].position[0] = msgData["movedTo"]
            # print("player position changed")

    """
    Name: updClients
    Parameters: conn: object, msgType: str, data: any
    Returns: None
    Purpose: Updates all other connections on the message the server has just recieved
    """

    def __updClients(self, conn, msgType: str, data) -> None:
        for client in self.__clientList:
            if (
                client is not None
                and client.client != conn
                and (
                    msgType != "platformInfo"
                    or msgType != "legalCheck"
                    or msgType != "leaderUpd"
                    or msgType != "leaderGet"
                )
            ):
                client.client.send(data)

            self.__sentMsg = True


if __name__ == "__main__":
    logPath: str = generateLogFile("server")

    server = Server(logPath)
    server.start()
