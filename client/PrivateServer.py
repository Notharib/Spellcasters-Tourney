import socket, json, threading, time
from random import randint, choice

class Client:
    def __init__(self, conn, spawnPoint):
        self.__client = conn
        self.__spawnPoint = spawnPoint
        self.__element = None
        self.__spellCaster = None

    def setElement(self, element):
        self.__element = element

    def setSpellCaster(self, spellCaster):
        self.__spellCaster = spellCaster

    def getSpawnPoint(self):
        return self.__spawnPoint

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
                threading.Thread(target=self.recv_from_client, args=(conn,)).start()
            if len(self.__clientList) >= self.__maxClients:
                self.beginGame()

    def beginGame(self):

        messageDict = {
            "type": "beginGame",
            "data": {
                "platformsPos": self.platformPositions,
                "playerSpawnPoint": None
            }
        }
        for client in self.__clientList:
            pass


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