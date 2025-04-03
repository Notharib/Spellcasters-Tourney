import socket, json, threading

class Client:
    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 50000
        self.clientNo = None
        self.__socket = None
        self.__noOfPlatforms = 0

    def connect(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__HOST, self.__PORT))


    def sendData(self,message):
        strMessage = json.dumps(message)
        self.__socket.send(strMessage.encode())

    def listen(self):
        while True:
            data = self.__socket.recv(1024)
            if not data:
                break
            else:
                try:
                    msg = dict(json.loads(data.decode()))

                    if msg["type"] == "clientNo":
                        print("client player created")
                        self.clientNo = msg["data"]["clientNo"]
                        return True, "addCharacter", msg["data"]
                    if msg["type"] == "playerJoin":
                        print("external player added")
                        return True, "addCharacter", msg["data"]
                    if msg["type"] == "movement":
                        return True, "movement", msg["data"]
                    if msg["type"] == "createPlat":
                        print("Created platform")
                        self.__noOfPlatforms += 1
                        msg["data"]["noOfPlats"] = self.__noOfPlatforms
                        return True, "createPlat", msg["data"]
                    if msg["type"] == "disconn":
                        print("Player Disconnected")
                        return True, "disconn", msg["data"]
                    if msg["type"] == "bullCreate":
                        return True, "bullCreate", msg["data"]
                    if msg["type"] == "MOVELEGAL":
                        return True, "legalMove", 1
                    if msg["type"] == "MOVENOTLEGAL":
                        return True, "illegalMove", 0

                except json.JSONDecodeError as err:
                    print(data.decode())
                    print("JSON Syntax Error:", err)

    def tellServerDisconn(self):
        msgDict = {"type":"disconn", "data":{"clientNo":self.clientNo}}
        self.sendData(msgDict)

if __name__ == "__main__":
    pass