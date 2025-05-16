import socket, json, threading, time
from random import randint, choice

# Client class, exclusive to server files. Done to try and make managing data surrounding the client connections easier. Purely only used within this file
class Client:
    def __init__(self, conn, spawnPoint, playerNo):
        self.__client = conn
        self.__spawnPoint = spawnPoint
        self.__element = None
        self.__spellCaster = None
        self.__playerNo = playerNo
        self.__colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.position = list(spawnPoint)

    def sendData(self, msgToSend):
        self.__client.send(msgToSend)

    # Getters and setters
    def setElement(self, element):
        self.__element = element

    def setSpellCaster(self, spellCaster):
        self.__spellCaster = spellCaster

    def getSpawnPoint(self):
        return self.__spawnPoint

    def getClient(self):
        return self.__client

    def getPlayerNo(self):
        return self.__playerNo

    def getElement(self):
        return self.__element

    def getPlayerColour(self):
        return self.__colour

    def getCaster(self):
        return self.__spellCaster

# Server class; modified from the public version to make it more suited to how a private game would function (e.g. max amount of clients, length of game)
class Server:
    def __init__(self, maxClients, lengthOfGame, platformPositions):
        self.__HOST = socket.gethostbyname(socket.gethostname())
        self.__PORT = 50001
        self.__clientList = []
        self.__maxClients = int(maxClients)
        self.__lengthOfGame = int(lengthOfGame)
        self.__platformPositions = platformPositions
        self.password = None

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__HOST, self.__PORT))
            s.listen(1)
            print("Server Setup and listening on port", self.__PORT)
            print(self.__maxClients)

            self.__spawnPoints = []
            for i in range(len(self.__platformPositions)):
                self.__spawnPoints.append((self.__platformPositions[i][0], self.__platformPositions[i][1]+20))

            # Should only accept new connections while the length of the client lists is less than the max number of connections
            while len(self.__clientList) < self.__maxClients:
                conn, addr = s.accept()
                print("New Connection from ", addr)

                colour = (randint(0, 255), randint(0, 255), randint(0, 255))
                position = choice(self.__spawnPoints)
                clientNoMessage = json.dumps({"type": "clientNo",
                                              "data": {"clientNo": len(self.__clientList) + 1, "colourTuple": colour,
                                                       "positionList": position}})
                print(clientNoMessage)
                conn.send(clientNoMessage.encode())
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

    # Starts a Thread to continue listening from the client until the server closes
    def startListening(self, conn):
            threading.Thread(target=self.recv_from_client, args=(conn,)).start()

    # Sends each client connection the required information for the clientside game to be able to generate properly
    def beginGame(self):

        messageDict = {
            "type": "beginGame",
            "data": {
                "platformsPos": self.__platformPositions,
                "positionList": None,
                "clientNo": None,
                "colourTuple": None,
                "otherPlayersInfo": {}
            }
        }

        # Sends each of the clients the information that they will need to create the stage and all of the opponents
        for client in self.__clientList:

            messageDict["data"]["positionList"] = client.getSpawnPoint()
            messageDict["data"]["clientNo"] = client.getPlayerNo()
            messageDict["data"]["colourTuple"] = client.getPlayerColour()

            for connection in self.__clientList:
                if connection != client:
                    messageDict["data"]["otherPlayersInfo"][connection.getPlayerNo()] = {
                        "type": connection.getCaster(),
                        "element": connection.getElement(),
                        "positionList": connection.getSpawnPoint(),
                        "colourTuple": connection.getPlayerColour(),
                        "clientNo": connection.getPlayerNo()
                    }


            client.sendData(json.dumps(messageDict).encode())
            messageDict = {
                "type": "beginGame",
                "data": {
                    "platformsPos": self.__platformPositions,
                    "positionList": None,
                    "clientNo": None,
                    "colourTuple": None,
                    "otherPlayersInfo": {}
                }
            }

    # Receives JSON formatted data from clients, sends to all other clients in the client list (except for certain circumstances)
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
                                clPos = client.getPlayerNo() - 1

                        if message["data"]["direction"] == "y":
                            self.__clientList[clPos].position[1] = message["data"]["movedTo"]
                            # print("changed player position")
                        else:
                            self.__clientList[clPos].position[0] = message["data"]["movedTo"]
                            # print("player position changed")
                    if message["type"] == "disconn":
                        self.tellClientsOfDisconn(message["data"]["clientNo"] - 1)
                        self.__clientList[message["data"]["clientNo"] - 1].client.close()
                        self.__clientList.pop(message["data"]["clientNo"] - 1)
                        print("player disconnected")

                    if message["type"] == "platformInfo":
                        iterator = 0
                        for platform in message["data"]:
                            self.__platforms[iterator].top = platform["platformTop"]
                            self.__platforms[iterator].bottom = platform["platformBottom"]
                            self.__platforms[iterator].left = platform["platformLeft"]
                            self.__platforms[iterator].right = platform["platformRight"]
                            iterator += 1

                    if message["type"] == "legalCheck":
                        messageData = message["data"]
                        clientMove = self.__clientList[messageData["clientNo"] - 1]
                        closestPlat = None
                        for platform in self.__platformPositions:
                            if closestPlat is None:
                                closestPlat = platform
                            else:
                                if messageData["direction"] == "y":
                                    if (platform.top >= clientMove.position[1] - messageData[
                                        "amount"] or platform.top <= clientMove.position[1] - messageData[
                                            "amount"]) and closestPlat.top - platform.top < 0:
                                        closestPlat = platform
                                else:
                                    if (platform.top >= clientMove.position[0] - messageData[
                                        "amount"] or platform.top <= clientMove.position[0] - messageData[
                                            "amount"]) and closestPlat.top - platform.top < 0:
                                        closestPlat = platform

                        if closestPlat is not None:
                            if messageData["direction"] == "y":
                                if clientMove.position[1] - messageData["amount"] <= closestPlat.position[1] + \
                                        closestPlat.platformSize[0]:
                                    clientMove.sendData(json.dumps({"type": "MOVENOTLEGAL"}).encode())
                                else:
                                    clientMove.sendData(json.dumps({"type": "MOVELEGAL"}).encode())
                            else:
                                if clientMove.position[0] - messageData["amount"] + clientMove.size[0] == \
                                        closestPlat.position[0] or clientMove.position[0] - messageData["amount"] <= \
                                        closestPlat.position[0] + closestPlat.platformSize[1]:
                                    clientMove.sendData(json.dumps({"type": "MOVENOTLEGAL"}).encode())
                                else:
                                    clientMove.sendData(json.dumps({"type": "MOVELEGAL"}).encode())
                    for client in self.__clientList:
                        if client is not None and client.getClient() != conn and (
                                message["type"] != "platformInfo" or message["type"] != "legalCheck"):
                            client.sendData(data)
                except json.JSONDecodeError as err:
                    print(data.decode())
                    print("JSON Syntax Error:", err)