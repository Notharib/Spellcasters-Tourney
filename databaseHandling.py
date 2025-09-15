import sqlite3

'''
Name: runsql
Parameters: *args: any
Returns: list[any]
Purpose: To run SQL statements
in the database
'''
def runsql(*args) -> list[any]:
    conn = sqlite3.connect("enc.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    if len(args) == 1:
        cursor.execute(args[0])
    else:
        cursor.execute(args[0], args[1])
    conn.commit()
    return cursor.fetchall()

'''
Name: tableCreate
Parameters: None
Returns: None
Purpose: Creates the initial table 
where the data is stored
'''
def tableCreate() -> None:
    sqlstring: str = """
    CREATE TABLE IF NOT EXISTS words (
        wordID INT AUTO_INCREMENT PRIMARY KEY,
        word TEXT
        )
    """

    runsql(sqlstring)

'''
Name: checkIfInDatabase
Parameters: word: str
Returns: bool
Purpose: Checks if a certain word is in
the database
'''
def checkIfInDatabase(word: str) -> bool:
    sqlstring: str = """
    SELECT word
    FROM words
    WHERE word == ?
    """
    values = (word, )
    data: list = runsql(sqlstring, values)
    data.append(None)
    
    if data[0] is None:
        return False
    else:
        return True

'''
Name: addToDatabase
Parameters: word: str
Returns: None
Purpose: Adds a word into the database
'''
def addToDatabase(word) -> None:
    sqlstring: str = """
    INSERT INTO words
    VALUES (?)
    """
    values = (word,)
    runsql(sqlstring, values)

'''
Name: getWord
Parameters: wordID: int
Returns: str
Purpose: Gets the word from the associated ID
'''
def getWord(wordID) -> str:
    sqlstring: str = """
    SELECT word
    FROM words
    WHERE wordID = ?
    """
    values = (wordID,)
    data: list = runsql(sqlstring, values)
    return data[0]
 
'''
Name: getWordID
Parameters: word: str
Returns: int
Purpose: Gets the ID of the word
'''
def getWordID(word) -> int:
    sqlstring: str = """
    SELECT wordID
    FROM words
    WHERE word = ?
    """
    values = (word,)
    data: list = runsql(sqlstring, values)
    
    return data[0]

if __name__ == "__main__":
    tableCreate()