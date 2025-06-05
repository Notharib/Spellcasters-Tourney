import socket, json, threading, random, time, requests

'''
Name: Client
Purpose: Client class for the private server, to make managing data about 
any given player easier
'''
class Client:
    def __init__(self, position,colour,cl,clientNo, address, size=[40,40]):
        self.addr = address
        self.client = cl
        self.position = position
        self.colour = colour
        self.clientNo = clientNo
        self.size = size

'''
Name: Platform
Purpose: To have platforms that players are able to move around on
'''
class Platform:
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
    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 50000
        self.__clientList = []
        self.__spawnPoints = [[250,250], [350,350],[450,450]]
        self.__platforms = [Platform([300,200],0),Platform([200,300],1)]


    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__HOST, self.__PORT))
            s.listen(1)
            print("Server Setup and listening on port", self.__PORT)
            while True:
                conn, addr = s.accept()
                print("New Connection from ", addr)

                colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                position = random.choice(self.__spawnPoints)
                clientNoMessage = json.dumps({"type":"clientNo","data":{"clientNo":len(self.__clientList)+1,"colourTuple": colour, "positionList":position}})
                print(clientNoMessage)
                conn.send(clientNoMessage.encode())
                time.sleep(0.1)

                if len(self.__clientList) != 0:
                    self.createAlreadyJoinedPlayers(conn)

                self.checkIfFull()

                self.__clientList.append(Client(position,colour,conn,len(self.__clientList)+1,addr))
                time.sleep(0.1)
                self.notifyClientsOfConn(conn,colour,position)
                self.createStage(conn)
                threading.Thread(target=self.recv_from_client, args=(conn,)).start()

    def notifyClientsOfConn(self,connection,colour,position):
        for client in self.__clientList:
            if client.client != connection:
                message = json.dumps({"type":"playerJoin","data":{"clientNo":len(self.__clientList)+1, "colourTuple": colour, "positionList":position}})
                client.client.send(message.encode())

    def checkIfFull(self):
        if len(self.__clientList) == 10:
            msg = requests.post(url="http://127.0.0.1:5000/serverFull", json={"fullValue":"1"})

    def createAlreadyJoinedPlayers(self,connection):
        for client in self.__clientList:
            message = json.dumps({"type": "playerJoin","data": {"clientNo": client.clientNo, "colourTuple": client.colour,"positionList": client.position}})
            connection.send(message.encode())
            time.sleep(0.2)

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

    def tellClientsOfDisconn(self,clientToDisconn):
        msg = requests.post(url="http://127.0.0.1:5000/serverFull", json={"fullValue":"0"})
        for client in self.__clientList:
            if client != self.__clientList[clientToDisconn] and client is not None:
                messageDict = {"type":"disconn","data":{"clientNo":clientToDisconn}}
                client.client.send(json.dumps(messageDict).encode())

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
                            if client.client == conn:
                                clPos = client.clientNo-1


                        if message["data"]["direction"] == "y":
                            self.__clientList[clPos].position[1] = message["data"]["movedTo"]
                            # print("changed player position")
                        else:
                            self.__clientList[clPos].position[0] = message["data"]["movedTo"]
                            # print("player position changed")
                    if message["type"] == "disconn":
                        self.tellClientsOfDisconn(message["data"]["clientNo"]-1)
                        self.__clientList[message["data"]["clientNo"]-1].client.close()
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
                        clientMove = self.__clientList[messageData["clientNo"]-1]
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
                        if client is not None and client.client != conn and (message["type"] != "platformInfo" or message["type"] != "legalCheck"):
                            client.client.send(data)
                except json.JSONDecodeError as err:
                    print(data.decode())
                    print("JSON Syntax Error:", err)


if __name__ == '__main__':
    server = Server()
    server.start()
