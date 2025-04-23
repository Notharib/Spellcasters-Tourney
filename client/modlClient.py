import socket, threading, time, json

class Client:
    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 50000

    def connect(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__HOST, self.__PORT))
        threading.Thread(target=self.listen).start()

    def listen(self):
        while True:
            data = self.__socket.recv(1024)
            if not data:
                break
            else:
                try:
                    msg = dict(json.loads(data.decode()))
                    print(msg)

                except json.JSONDecodeError as err:
                    print(data.decode())
                    print("JSON Syntax Error:", err)

                except Exception as e:
                    print("Error:", e)