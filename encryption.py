import random

from databaseHandling import checkIfInDatabase, addToDatabase, getWord, getWordID

alphabet: list[str] = "a b c d e f g h i j l k m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z { } [ ] ' : ".split(" ")
alphabet.append(" ")

numToLet: dict = {}
letToNum: dict = {}
for i in range(len(alphabet)):
    numToLet[i] = alphabet[i]
    letToNum[numToLet[i]] = i


def is_prime(number: int, divider: int = 2) -> bool:
    '''
    Name: is_prime
    Parameters: number: int, divider: int
    Returns: bool
    Purpose: Checks if the number entered is prime
    '''
    if divider > number ** 0.5:
        return True
    if number % divider == 0:
        return False
    return is_prime(numbder, divider=divider+1)


def generateRandomPrime(length:int) -> int:
    '''
    Name: generateRandomPrime
    Parameters: length:int
    Returns: retVal: int
    Purpose: Generates a random prime number, that is
    the length of the parameter
    '''
    retVal: int = random.randint(2**length, 2**length +1)
    while not is_prime(retVal):
        retVal = random.randint(2**(length // 2), 2**(length // 2 +1))
    return retVal

def generateGCD(a: int, b: int) -> int:
    '''
    Name: generateGCD
    Parameters: a: int, b:int
    Returns: int
    Purpose: Generates the Greatest Common Divider between
    two numbers using Euclid's Algorithm
    '''
    if a == b:
        return a
    elif a > b:
        return generateGCD(a-b, b)
    elif a < b:
        return generateGCD(a, b-a)

def test_congruence(mod:int):
    '''
    Name: test_congruence
    Parameters: mod:int
    Returns: function
    Purpose: Returns a lambda function to predetermine the mod value
    for testing congruence between two values
    '''
    return lambda a, b: a % mod == b % mod 


def generateMMI(a: int, b: int) -> int:
    '''
    Name: generateMMI
    Parameters: a: int, b:int
    Returns: retVal: int
    Purpose: Generates the Modular Multiplicative Inverse
    of two numbers
    '''
    retVal: int = 2

    congruent: bool = test_congruence(b)

    while True:
        if congruent(1, (a*retVal)):
            return retVal
        else:
            retVal += 1

def generateLCM(a: int, b: int) -> int:
    '''
    Name: generateLCM 
    Parameters: a: int, b: int
    Returns: int
    Purpose: Generates the Least Common Multiple
    of two numbers
    '''
    if a / -1 > 0:
        a /= -1
    if b / -1 > 0:
        b /= -1
    return a * (b / generateGCD(a,b))

def generateCoPrime(b: int, a: int = 2) -> int:
    '''
    Name: generateCoPrime
    Parameters: b: intt, a: int
    Returns: retVal: int
    Purpose: Generates a coprime for two numbers
    '''
    retVal: int = a
    while generateGCD(retVal, b) != 1:
        retVal += 1
    return retVal

def encrypt(message: str, e: int, n: int) -> int:
    '''
    Name: encrypt
    Parameters: message: str, e: int, n: int
    Returns: int
    Purpose: Encrypts a message using the given values
    '''
    if not checkIfInDatabase(message):
        addToDatabase(message)
    
    return (getWordID(message) ** e) % n

def decrypt(message: int, d: int, n: int) -> str:
    '''
    Name: decrypt
    Parameters: message: int, d: int, n:int
    Returns: int
    Purpose: Decrypts a message using the given values
    '''
    orgID: int = (message ** d) % n

    return getWord(orgID)

def generateKeyPair(key_length: int) -> dict:
    '''
    Name: generateKeyPair
    Parameters: key_length: int
    Returns: keys:dict
    Purpose: Generates a public and a private encryption key
    '''

    keys: int = {}

    p: int = generateRandomPrime(key_length // 2)
    q: int = generateRandomPrime(key_length // 2)

    while p == q:
        q = generateRandomPrime(key_length //2)
    
    n = p * q
    phi_n = generateLCM(p-1, q-1)

    e: int = generateRandomCoPrime(phi_n)

    d: int = generateMMI(e, phi_n)

    keys["public"] = e
    keys["private"] = d
    keys["n"] = n

    return keys



