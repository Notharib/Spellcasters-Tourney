from time import time
from random import randint

import os

"""
Name: generateLogFile
Parameters: origin: str
Returns: fileName: str
Purpose: Generates a file (and a directory if it doesn't exist)
that a service (such as a client/the server/the API) that the service can use
to store error messages, making it easier to debug issues
"""


def generateLogFile(origin: str) -> str:
    # Makes the log directory in case it doesn't exist
    os.makedirs(f"{origin}Logs/", exist_ok=True)

    generated: bool = False
    while not generated:
        try:
            fileName: str = os.path.join(
                f"{origin}Logs/", f"{origin}{str(generateLogID())}.log"
            )
            f = open(fileName, "x")
            f.close()
            generated = True

        except Exception as e:
            # On the rare occasion that the logID is already in use, it will simply just generate a new ID
            generated = False
    print(f"Run Log Generated at {origin}Logs/, filename {fileName}")
    return fileName


"""
Name: generateLogID
Paramaters: None
Returns: int
Purpose: Generates a logID integer to be used
"""


def generateLogID() -> int:
    timeOfCreation: float = time()
    pi: float = 3.141592653589

    # The reason this number is used is because it means that the number is
    # at least partially based off of the time it was generated, making the generation
    # of duplicates far less likely
    return round(timeOfCreation / pi / 1000) + randint(1, 10000)


"""
Name: addToLog
Parameters: logFile: str, errOrg: str, errMsg: str, extraInfo: str
Returns: None
Purpose: Adds an error message, and the function/object that it happened
in, to a log file
"""


def addToLog(logFile: str, errOrg: str, errMsg: str = "", extraInfo: str = "") -> None:
    fullMsg: str = errOrg.upper() + extraInfo + ": " + str(errMsg)
    print(f"\n{fullMsg}")
    try:
        with open(logFile, "a") as file:
            file.write(f"\n{fullMsg}")
            file.close()
    except Exception as e:
        with open(logFile, "w") as file:
            file.write(fullMsg)
            file.close()

