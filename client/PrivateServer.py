import socket, json, threading, time
from random import randint, choice

# Platform class for exclusive use in the private server
class Platform:
    def __init__(self, position, size=[20,500]):
        self.__position = position
        self.__size = size
        self.__colour = (0,0,255)
        self.__top = None
        self.__left = None
        self.__right = None
        self.__bottom = None

    # Getters and Setters
    def getPos(self):
        return self.__position
    def getSize(self):
        return self.__size
    def getTop(self):
        return self.__top
    def getBottom(self):
        return self.__bottom
    def getLeft(self):
        return self.__left
    def getRight(self):
        return self.__right
    def setTop(self, top):
        self.__top = top
        return None
    def setLeft(self, left):
        self.__left = left
        return None
    def setRight(self, right):
        self.__right = right
        return None
    def setBottom(self, bottom):
        self.__bottom = bottom
        return None

    def __repr__(self):
        return self.__position

# Client class, exclusive to server files. Done to try and make managing data surrounding the client connections easier. Purely only used within this file
class Client:
    def __init__(self, conn, spawnPoint, playerNo, size=[40,40]):
        self.__client = conn
        self.__spawnPoint = spawnPoint
        self.__element = None
        self.__spellCaster = None
        self.__playerNo = playerNo
        self.__colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.position = list(spawnPoint)
        self.__size = size

    def sendData(self, msgToSend):
        self.__client.send(msgToSend)

    # Getters and setters
    def setElement(self, element):
        self.__element = element

    def setSpellCaster(self, spellCaster):
        self.__spellCaster = spellCaster

    def getSpawnPoint(self):
        return self.__spawnPoint

    def getSize(self):
        return self.__size

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
        self.__platforms = []
        self.__spawnPoints = []
        self.password = None

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
                # clientNoMessage = json.dumps({"type": "clientNo",
                #                               "data": {"clientNo": len(self.__clientList) + 1, "colourTuple": colour,
                #                                        "positionList": position}})
                # print(clientNoMessage)
                # conn.send(clientNoMessage.encode())
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

            # print(messageDict)
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

    # Handles what to do with the data it receives
    def __messageHandling(self, message, conn):
        try:
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
                clientMove = self.__clientList[messageData["clientNo"] - 1]
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

    # Receives JSON formatted data from clients, sends to all other clients in the client list (except for certain circumstances)
    def recv_from_client(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                try:
                    # message = dict(json.loads(data.decode()))
                    decodedData = data.decode()
                    message = dict(json.loads(decodedData))
                    self.__messageHandling(message, conn)

                except json.JSONDecodeError as e:
                    print("json extra data handling",e)
                    for decodedMsg in data.decode():
                        try:
                            message = json.loads(decodedMsg)
                            self.__messageHandling(message,conn)
                        except Exception as e:
                            print("Error:", e)
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