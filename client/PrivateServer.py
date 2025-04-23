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

    def getCaster(self):
        return self.__spellCaster

# Server class; modified from the public version to make it more suited to how a private game would function (e.g. max amount of clients, length of game)
class Server:
    def __init__(self, maxClients, lengthOfGame, platformPositions):
        self.__HOST = '127.0.0.1'
        self.__PORT = 50000
        self.__clientList = []
        self.__maxClients = maxClients
        self.__lengthOfGame = lengthOfGame
        self.__platformPositions = platformPositions

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__HOST, self.__PORT))
            s.listen(1)
            print("Server Setup and listening on port", self.__PORT)

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
                self.__clientList.append(conn)
                # Separate function used so that it will still continue running after the while loop in this function stops running
                self.startListening(conn)

            # Once the required number of clients has joined, send the start information to all the clients in '__clientList'
            if len(self.__clientList) >= self.__maxClients:
                self.beginGame()

    def startListening(self, conn):
        while True:
            threading.Thread(target=self.recv_from_client, args=(conn,)).start()

    # Sends each client connection the required information for the clientside game to be able to generate properly
    def beginGame(self):

        messageDict = {
            "type": "beginGame",
            "data": {
                "platformsPos": self.__platformPositions,
                "playerSpawnPoint": None,
                "otherPlayersInfo": {}
            }
        }

        # Sends each of the clients the information that they will need to create the stage and all of the opponents
        for client in self.__clientList:
            messageDict["data"]["playerSpawnPoint"] = client.getSpawnPoint()
            for connection in self.__clientList:
                if connection != client:
                    messageDict["data"]["otherPlayersInfo"][connection.getPlayerNo()] = {
                        "type": connection.getCaster(),
                        "element": connection.getElement()
                    }

    # Receives JSON formatted data from clients, sends to all other clients in the client list (except for certain circumstances)
    def recv_from_client(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                try:
                    for client in self.__clientList:
                        if client is not None and client != conn:
                            client.send(data)
                except json.JSONDecodeError as err:
                    print(data.decode())
                    print("JSON Syntax Error:", err)