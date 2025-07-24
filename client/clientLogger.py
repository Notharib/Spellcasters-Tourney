import math
import os
import time
import random


class Logger:
    def __init__(self) -> None:
        self.__timeOfCreation = time.time()
        self.__ID = int(round(self.__timeOfCreation // math.pi //1000) + random.randint(1,10000)

        os.makedirs('clLogs/', exist_ok=True)

        self.__file = os.path.join('clLogs/', f'client{self.__ID}.log')
        print(f"Client log created with ID no.{self.__ID}")
        f = open(self.__file, 'x')
        f.close()

    def addToLog(self, data: str) -> None:
        try:
            with open(self.__file, 'a') as file:
                file.write(f"\n{data}")
                file.close()
        except Exception as e:
            with open(self.__file, 'w') as file:
                file.write(f"{data}")
                file.close()

    def logDump(self) -> None:
        with open(self.__file, "r") as file:
            content = file.read()
            print(content)
            file.close()
