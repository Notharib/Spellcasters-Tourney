import socket, json, threading, pygame, random

class Server:
    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 50000
        self.__clientList = []
        self.__spawnPoints = [(200,200), (300,300),(250,250)]


    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__HOST, self.__PORT))
            s.listen(1)
            print("Server Setup and listening on port", self.__PORT)
            while True:
                conn, addr = s.accept()
                print("New Connection from ", addr)
                self.__clientList.append(conn)
                colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                position = random.choice(self.__spawnPoints)
                clientNoMessage = json.dumps({"type":"clientNo","data":{"clientNo":len(self.__clientList)+1,"colour": colour, "position":position}})
                print(clientNoMessage)
                conn.send(clientNoMessage.encode())
                threading.Thread(target=self.recv_from_client, args=(conn,)).start()

    def notifyClientsOfConn(self,connection,colour,position):
        for client in self.__clientList:
            if client != connection:
                message = json.dumps({"type":"playerJoin","data":{"clientNo":len(self.__clientList)+1, "colour": colour, "position":position}})
                client.send(message.encode())

    def recv_from_client(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                print(data.decode())
                for client in self.__clientList:
                    if client != conn:
                        client.send(data)


if __name__ == '__main__':
    server = Server()
    server.start()
