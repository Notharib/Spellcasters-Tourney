import time, math

class Logger:
    def __init__(self) -> None:
        self.__timeOfCreation = time.time()
        self.__ID = self.__timeOfCreation // math.pi //1000
        self.__file = f'clLogs/client{self.__ID}.log'
        print(f"Client log created with ID no. {self.__ID}")

    def addToLog(self, data: str) -> None:
        with open(self.__file, 'a') as file:
            file.write("\ndata")
            file.close()

    def logDump(self) -> None:
        with open(self.__file, "r") as file:
            content = file.read()
            print(content)
            file.close()
