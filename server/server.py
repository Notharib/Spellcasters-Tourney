import json
import random
import socket
import threading
import time

import requests

'''
Name: Client
Purpose: Client class for the private server, to make managing data about 
any given player easier
'''
class Client:
    '''
    Name: __init__
    Parameters: position:list, colour:tuple, cl:object, playerID:integer, address:string, size:list
    Returns: None
    Purpose: Constructor to set the initial values
    of the Client object
    '''
    def __init__(self, position,colour,cl,playerID, address, size=[40,40]):
        self.__addr: str = address
        self.__client = cl
        self.__position: list[int] = position
        self.__colour: tuple[int,int,int] = colour
        self.__playerID: int = playerID
        self.__size: list[int] = size

    '''
    Name: sendData
    Parameters: message:str
    Returns: None
    Purpose: Sends data to the client
    '''
    def sendData(self, message: str) -> None:
        self.__conn.send(message.encode())

    '''
    Name: getPlayerID
    Parameters: None
    Returns: self.__playerID: int
    Purpose: Getter for the client's playerID
    '''
    def getPlayerID(self) -> int:
        return self.__playerID

    '''
    Name: getPosition
    Parameters: None
    Returns: self.__position:list[int]
    Purpose: Getter for the client's position
    '''
    def getPosition(self) -> list[int]:
        return self.__position

    '''
    Name: getClient 
    Parameters: None
    Returns: self.__client:object
    Purpose: Getter for the client's client
    '''
    def getClient(self) -> any:
        return self.__client

    '''
    Name: setPosition
    Parameters: position:list[int]
    Returns: None
    Purpose: Setter for the client's position
    '''
    def setPosition(self, position: list[int]) -> None:
        self.__position = position

'''
Name: Platform
Purpose: To have platforms that players are able to move around on
'''
class Platform:
    '''
    Name: __init__
    Parameters: position:list, platformId: integer, colour:tuple, platformSize:list
    Returns: None
    Purpose: Constructor to set the initial values
    of the Platform object
    '''
    def __init__(self, position, platformId, colour=(0,255,0),platformSize=[20,500]):
        self.position = position
        self.colour = colour
        self.platformSize = platformSize
        self.platformId = platformId
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None

'''
Name: Server
Purpose: Server class to handle connections from the different clients. Different to the private server's
Server class, due to the differences in functionality required from both of them
'''
class Server:
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Server object
    '''
    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 50000
        self.__clientList = []
        self.__spawnPoints = [[250,250], [350,350],[450,450]]
        self.__platforms = [Platform([300,200],0),Platform([200,300],1)]
        self.__leaderboard = {}

    '''
    Name: start
    Parameters: None
    Returns: None
    Purpose: Starts listening for new connections from clients, and handles what to do with them upon joining
    '''
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__HOST, self.__PORT))
            s.listen(1)
            print("Server Setup and listening on port", self.__PORT)
            while True:
                conn, addr = s.accept()
                print("New Connection from ", addr)

                # Sends the client the information they will initially need so that they can join the server properly
                colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                position = random.choice(self.__spawnPoints)
                playerIDMessage = json.dumps({"type":"playerID","data":{"playerID":len(self.__clientList)+1,"colourTuple": colour, "positionList":position}})
                print(playerIDMessage)
                conn.send(playerIDMessage.encode())
                time.sleep(0.1)

                if len(self.__clientList) != 0:
                    self.createAlreadyJoinedPlayers(conn)

                # Checks if the server is now full (aka reached 10 active players)
                self.checkIfFull()

                self.__clientList.append(Client(position,colour,conn,len(self.__clientList)+1,addr))
                self.__leaderboard[len(self.__clientList)+1] = 0
                time.sleep(0.1)
                self.notifyClientsOfConn(conn,colour,position)
                self.createStage(conn)
                threading.Thread(target=self.recv_from_client, args=(conn,)).start()

    '''
    Name: notifyClientsOfConn
    Parameters: connection:object, colour:tuple, position:list
    Returns: None
    Purpose: Lets all clients in the self.__clientList variable know that a new client has joined, 
    as well as sending them the character data required for the character to be created
    '''
    def notifyClientsOfConn(self,connection,colour,position):
        self.leaderUpd(len(self.__clientList))
        for client in self.__clientList:
            if client.client != connection:
                message = json.dumps({"type":"playerJoin","data":{"playerID":len(self.__clientList)+1, "colourTuple": colour, "positionList":position}})
                client.client.send(message.encode())

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
    Name: checkIfFull
    Parameters: None
    Returns: None
    Purpose: Checks if the server is at max capacity (10 active connections), and then if it is, letting the API know
    that it is full so it shouldn't let any more players join
    '''
    def checkIfFull(self):
        if len(self.__clientList) == 10:
            msg = requests.post(url="http://127.0.0.1:5000/serverFull", json={"fullValue":"1"})

    '''
    Name: createAlreadyJoinedPlayers
    Parameters: connection:object
    Returns: None
    Purpose: Sends the newly joined player all the clients' information to ensure that they are not out of sync
    '''
    def createAlreadyJoinedPlayers(self,connection):
        for client in self.__clientList:
            message = json.dumps({"type": "playerJoin","data": {"playerID": client.playerID, "colourTuple": client.colour,"positionList": client.position}})
            connection.send(message.encode())
            time.sleep(0.2)

    '''
    Name: createStage
    Parameters: connection:object
    Returns: None
    Purpose: Sends all the platform information to the newly joined client
    '''
    def createStage(self,connection):
        platformSize = [20,500]
        platformPositions =[[300,200],[200,300]]
        iterator = 0
        for position in platformPositions:
            positionX = position[0]
            positionY = position[1]
            positionMessage = json.dumps({"type":"createPlat", "data": {"positionX":positionX, "positionY":positionY, "sizeHeight":platformSize[0],"sizeWidth":platformSize[1], "platformNo":iterator}})
            connection.send(positionMessage.encode())
            iterator += 1
            time.sleep(0.2)

    '''
    Name: tellClientsOfDisconn
    Parameters: clientToDisconn
    Returns: None
    Purpose: Lets all clients in the self.__clientList variable know that a client has disconnected, and that
    they need to remove that client from their sprite group in order to stay in sync. Also lets the API know that the
    server isn't full
    '''
    def tellClientsOfDisconn(self,clientToDisconn):
        msg = requests.post(url="http://127.0.0.1:5000/serverFull", json={"fullValue":"0"})
        for client in self.__clientList:
            if client != self.__clientList[clientToDisconn] and client is not None:
                messageDict = {"type":"disconn","data":{"playerID":clientToDisconn}}
                client.client.send(json.dumps(messageDict).encode())

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
    Name: leaderUpd
    Parameters: None
    Returns: None
    Purpose: Sends a POST request to the API to update the information on the public leaderboard
    '''
    def leaderUpd(self, playerID):
        requests.post(url="http://127.0.0.1:5000/publicLeaderUpd", json={"playerID":playerID})

    '''
    Name: recv_from_client
    Parameters: conn:object
    Returns: None
    Purpose: Listens for data being sent by the connection, and then if data is sent, handles what
    to do with it
    '''
    def recv_from_client(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                try:
                    message = dict(json.loads(data.decode()))
                    if message["type"] == "leaderUpd":
                        #self.__leaderboard[message["data"]["playerID"]] += 1
                        self.leaderUpd(message["data"]["playerID"])
                    if message["type"] == "leaderGet":
                        leaderMsg = {
                            "type":"leaderGet",
                            "data": self.__leaderboard
                        }
                        conn.send(json.dumps(leaderMsg).encode())

                    if message["type"] == "movement":
                        for client in self.__clientList:
                            if client.client == conn:
                                clPos = client.playerID-1

                        self.__clientList[clPos].position[0], self.__clientList[clPos].position[1] = message["data"]["posX"], message["data"]["posY"]

                    if message["type"] == "disconn":
                        self.tellClientsOfDisconn(message["data"]["playerID"]-1)
                        self.__clientList[message["data"]["playerID"]-1].client.close()
                        self.__clientList.pop(message["data"]["playerID"] - 1)
                        print("player disconnected")

                    if message["type"] == "platformInfo":
                        iterator = 0
                        for platform in message["data"]:
                            self.__platforms[iterator].top = platform["platformTop"]
                            self.__platforms[iterator].bottom = platform["platformBottom"]
                            self.__platforms[iterator].left = platform["platformLeft"]
                            self.__platforms[iterator].right = platform["platformRight"]
                            iterator += 1

                    if message["type"] == "casterInfo":
                        data = message["data"]
                        clPos: int = self.__getClientPosition(conn)

                        self.__clientList[clPos].setElement(data["element"])
                        self.__clientList[clPos].setCaster(data["caster"])
                    
                    if message["type"] == "legalCheck":
                        messageData = message["data"]
                        clientMove = self.__clientList[messageData["playerID"]-1]
                        closestPlat = None
                        for platform in self.__platforms:
                            if closestPlat is None:
                                closestPlat = platform
                            else:
                                if messageData["direction"] == "y":
                                    if (platform.top >= clientMove.position[1]-messageData["amount"] or platform.top <= clientMove.position[1]-messageData["amount"]) and closestPlat.top - platform.top < 0:
                                        closestPlat = platform
                                else:
                                    if (platform.top >= clientMove.position[0]-messageData["amount"] or platform.top <= clientMove.position[0]-messageData["amount"]) and closestPlat.top - platform.top < 0:
                                        closestPlat = platform


                        if closestPlat is not None:
                            if messageData["direction"] == "y":
                                if clientMove.position[1] - messageData["amount"] <= closestPlat.position[1]+closestPlat.platformSize[0]:
                                    clientMove.client.send(json.dumps({"type":"MOVENOTLEGAL"}).encode())
                                else:
                                    clientMove.client.send(json.dumps({"type": "MOVELEGAL"}).encode())
                            else:
                                if clientMove.position[0] - messageData["amount"] + clientMove.size[0] == closestPlat.position[0] or clientMove.position[0] - messageData["amount"] <= closestPlat.position[0]+closestPlat.platformSize[1]:
                                    clientMove.client.send(json.dumps({"type":"MOVENOTLEGAL"}).encode())
                                else:
                                    clientMove.client.send(json.dumps({"type": "MOVELEGAL"}).encode())
                    for client in self.__clientList:
                        if (client is not None and client.client != conn and
                                (message["type"] != "platformInfo" or message["type"] != "legalCheck" or message["type"] != "leaderUpd" or
                                message["type"] != "leaderGet")):
                            client.client.send(data)
                except json.JSONDecodeError as err:
                    print(data.decode())
                    print("JSON Syntax Error:", err)


if __name__ == '__main__':
    server = Server()
    server.start()
