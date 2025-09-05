import json
import random
import socket
import threading
import time

import requests

from serverClasses import Client, Server

'''
Name: Server
Purpose: Server class to handle connections from the different clients. Different to the private server's
Server class, due to the differences in functionality required from both of them
'''
class PublicServer(Server):
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Server object
    '''
    def __init__(self):
        Server.__init__(self)
        self.__leaderboard: dict = {}
        

    '''
    Name: start
    Parameters: None
    Returns: None
    Purpose: Starts listening for new connections from clients, and handles what to do with them upon joining
    '''
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self._HOST, self._PORT))
            s.listen(1)
            print("Server Setup and listening on port", self._PORT)
            while True:
                conn, addr = s.accept()
                print("New Connection from ", addr)

                # Sends the client the information they will initially need so that they can join the server properly
                colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                position = random.choice(self._spawnPoints)
                playerIDMessage = json.dumps({"type":"playerID","data":{"playerID":len(self._clientList)+1,"colourTuple": colour, "positionList":position}})
                print(playerIDMessage)
                conn.send(playerIDMessage.encode())
                time.sleep(0.1)

                if len(self._clientList) != 0:
                    self.createAlreadyJoinedPlayers(conn)

                # Checks if the server is now full (aka reached 10 active players)
                self.checkIfFull()

                self._clientList.append(Client(conn, position, len(self._clientList)+1, colour))
                self.__leaderboard[len(self._clientList)+1] = 0
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
        self.leaderUpd(len(self._clientList))
        for client in self._clientList:
            if client.getClient() != connection:
                message = json.dumps({"type":"playerJoin","data":{"playerID":len(self._clientList)+1, "colourTuple": colour, "positionList":position}})
                client.client.send(message.encode())

    '''
    Name: checkIfFull
    Parameters: None
    Returns: None
    Purpose: Checks if the server is at max capacity (10 active connections), and then if it is, letting the API know
    that it is full so it shouldn't let any more players join
    '''
    def checkIfFull(self):
        if len(self._clientList) == 10:
            msg = requests.post(url="http://127.0.0.1:5000/serverFull", json={"fullValue":"1"})

    '''
    Name: createAlreadyJoinedPlayers
    Parameters: connection:object
    Returns: None
    Purpose: Sends the newly joined player all the clients' information to ensure that they are not out of sync
    '''
    def createAlreadyJoinedPlayers(self,connection):
        for client in self._clientList:
            message = json.dumps({"type": "playerJoin","data": {"playerID": client.getPlayerID(), "colourTuple": client.getColour(),"positionList": client.getPosition()}})
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
        for client in self._clientList:
            if client != self._clientList[clientToDisconn] and client is not None:
                messageDict = {"type":"disconn","data":{"playerID":clientToDisconn}}
                client.sendData(json.dumps(messageDict))

    '''
    Name: __getClientPosition
    Parameters: conn:object
    Returns: int
    Purpose: Gets the position of a certain client object within the clientList variable
    '''
    def __getClientPosition(self, conn) -> int:
        for client  in self._clientList:
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

    

if __name__ == '__main__':
    server = PublicServer()
    server.start()
