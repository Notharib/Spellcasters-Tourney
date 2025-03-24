import socket, json, threading, random, time

class Client:
    def __init__(self, position,colour,cl,clientNo):
        self.client = cl
        self.position = position
        self.colour = colour
        self.clientNo = clientNo

class Server:
    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 50000
        self.__clientList = []
        self.__spawnPoints = [[250,250], [350,350],[450,450]]


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

                self.__clientList.append(Client(position,colour,conn,len(self.__clientList)+1))
                time.sleep(0.1)
                self.createStage(conn)
                threading.Thread(target=self.recv_from_client, args=(conn,)).start()

    def notifyClientsOfConn(self,connection,colour,position):
        for client in self.__clientList:
            if client.client != connection:
                message = json.dumps({"type":"playerJoin","data":{"clientNo":len(self.__clientList)+1, "colourTuple": colour, "positionList":position}})
                client.client.send(message.encode())

    def createAlreadyJoinedPlayers(self,connection):
        for client in self.__clientList:
            message = json.dumps({"type": "playerJoin","data": {"clientNo": client.clientNo, "colourTuple": client.colour,"positionList": client.position}})
            connection.send(message.encode())
            time.sleep(0.2)

    def createStage(self,connection):
        platformSize = [20,500]
        platformPositions =[[300,200],[200,300],[500,200]]
        for position in platformPositions:
            positionX = position[0]
            positionY = position[1]
            positionMessage = json.dumps({"type":"createPlat", "data": {"positionX":positionX, "positionY":positionY, "sizeHeight":platformSize[0],"sizeWidth":platformSize[1]}})
            connection.send(positionMessage.encode())
            time.sleep(0.2)

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
                        else:
                            self.__clientList[clPos].position[0] = message["data"]["movedTo"]
                    for client in self.__clientList:
                        if client.client != conn:
                            client.client.send(data)
                except json.JSONDecodeError as err:
                    print(data.decode())
                    print("JSON Syntax Error:", err)


if __name__ == '__main__':
    server = Server()
    server.start()
