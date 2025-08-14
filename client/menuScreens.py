import socket

import pygame
import pygame.freetype
import requests
from characterCreation import Druid, Fire, Water, Wizard
from menuClasses import Pointer, TextBox

'''
Name: waiting
Parameters: c: object, screen: object, creationData: dictionary
Returns: None
Purpose: Run loop for a waiting screen while a player is waiting for other players to 
join their private server
'''
def waiting(c, screen, creationData):
    textOne = "Waiting for players to join!"
    textTwo = f"Join Code: {creationData['joinKey']}"
    textThree = f"Server Pin: {creationData['pinNo']}"

    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True

    c.enableWaiting()
    while c.checkWaiting():
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                c.waitingOver()
                exit()

        f.render_to(screen, (300, 300), textOne, (0, 0, 0))
        f.render_to(screen, (300, 350), textTwo, (0, 0, 0))
        f.render_to(screen, (300, 400), textThree, (0, 0, 0))
        pygame.display.flip()

'''
Name: gameStart
Parameters: screen: object
Returns: dictionary
Purpose: Pygame run loop that determines what the player wants to do, 
whether it be play on the public server, or join/create a private server
'''
def gameStart(screen):
    running = True
    textOne = "Welcome to Wizards Tourney. These are your options for playing:"
    textTwo = "1) Press P to join the public server"
    textThree = "2) Press A to join or create a private server"
    textFour = ""

    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True


    while running:

        while running:
            screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_p]:
                        serverFull = requests.get(url="http://127.0.0.1:5000/serverFullCheck").json()
                        if int(serverFull["quickMsg"]) == 1:
                            textFour = "The Public Server is full right now! Please try joining later"
                        else:
                            running = False
                            return {"type":"publicGame"}
                    elif keys[pygame.K_a]:
                         g = privateGame(screen)
                         return g

            f.render_to(screen,(50,300),textOne, (0,0,0))
            f.render_to(screen, (100, 400), textTwo, (0, 0, 0))
            f.render_to(screen, (100, 450), textThree, (0, 0, 0))
            f.render_to(screen, (100, 550), textFour, (0, 0, 0))
            pygame.display.update()
        return True

'''
Name: privateGame
Parameters: screen: object
Returns: dictionary | boolean
Purpose: Pygame run loop to allow the player to decide whether they wish to join a private
server or create one
'''
def privateGame(screen):
    textOne = "Do you wish to join or create a private server?"
    textTwo = "Press J to join one"
    textThree = "Press C to create one"

    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True

    running = True
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_c]:
                    createInfo = privateCreate(screen)
                    if createInfo is not None:
                        return createInfo
                if keys[pygame.K_j]:
                    joinInfo = enterPrivGameInfo(screen)
                    if joinInfo is not None:
                        return joinInfo

        f.render_to(screen, (50, 300), textOne, (0, 0, 0))
        f.render_to(screen, (100, 400), textTwo, (0, 0, 0))
        f.render_to(screen, (100, 450), textThree, (0, 0, 0))
        pygame.display.update()

'''
Name: privateCreate
Parameters: screen: object
Returns: dictionary
Purpose: Constructor to set the initial values
of the treasure object
'''
def privateCreate(screen):
    noOfPlayers = "EXAMPLE"
    textOne = "Enter number of players you wish to be able to join the private server: "

    gameLength = "EXAMPLE"
    textTwo = "Enter the amount of time you wish to have the game go on for: "

    textThree = "Press L when you wish to wait for players to start joining"

    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True

    pointer = pygame.sprite.Group()
    textBoxes = pygame.sprite.Group()

    pointer.add(Pointer())

    textBoxes.add(TextBox(position=(150,150), text=noOfPlayers, allow="numberInput"))
    textBoxes.add(TextBox(position=(100, 300), text=gameLength, allow="numberInput"))

    running = True
    while running:
        screen.fill((255, 255, 255))
        pygame.key.set_repeat(200)

        noOfPlayers = textBoxes.sprites()[0].text
        gameLength = textBoxes.sprites()[1].text

        keys = pygame.key.get_pressed()
        typ3 = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                # print("EVENT KEY PRESSED!!!!")
                keys = pygame.key.get_pressed()
                typ3 = pygame.key.get_pressed()
                if keys[pygame.K_l]:
                    # print("Private Game Made!")
                    pygame.key.set_repeat(0)
                    joinInfo = requests.post("http://127.0.0.1:5000/pItHv", json={"IPAddress":socket.gethostbyname(socket.gethostname())}).json()
                    print(joinInfo, type(joinInfo))
                    joinKey = joinInfo["hashedItem"]
                    pinNo = joinInfo["PIN"]
                    return {
                        "type": "privateCreate",
                        "data": {
                            "lengthOfGame": gameLength,
                            "noOfPlayers": noOfPlayers,
                            "joinKey": joinKey,
                            "pinNo": pinNo
                        }
                    }
            # if event.type == pygame.KEYUP:
            #     type = pygame.key.get_pressed()

        if typ3 is not None:
            collided = pygame.sprite.groupcollide(pointer, textBoxes, False, False)
            for p, t_List in collided.items():
                for tBox in t_List:
                    tBox.typing = True
                    tBox.update(typ3)
                    for textBox in textBoxes.sprites():
                        textBox.typing = False

        f.render_to(screen,(25,100),textOne, (0,0,0))
        f.render_to(screen, (150,150), noOfPlayers, (0, 0, 0))
        f.render_to(screen, (25, 250), textTwo, (0, 0, 0))
        f.render_to(screen, (100, 300), gameLength, (0, 0, 0))
        f.render_to(screen, (100, 550), textThree, (0, 0, 0))

        pointer.update()
        pointer.draw(screen)
        textBoxes.draw(screen)
        pygame.display.update()

'''
Name: enterPrivGameInfo
Parameters: screen: object
Returns: dictionary
Purpose: Pygame run loop to allow the player to enter the required information to join a private server
'''
def enterPrivGameInfo(screen):
    textOne = "Press ENTER to join the server!"
    textTwo = "Server Key: "
    textThree = ""
    textFour = "Server Pin:"

    serverKey = "EXAMPLE"
    serverPin = "EXAMPLE"

    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True

    pointer = pygame.sprite.Group()
    textBoxes = pygame.sprite.Group()

    pointer.add(Pointer())

    textBoxes.add(TextBox(position=(150, 200), text=serverKey, allow="textInput"))
    textBoxes.add(TextBox(position=(150, 300), text=serverPin, allow="numberInput"))

    running = True
    while running:
        screen.fill((255, 255, 255))

        serverKey = textBoxes.sprites()[0].text
        serverPin = textBoxes.sprites()[1].text

        pygame.key.set_repeat(200)

        keys = pygame.key.get_pressed()
        typ3 = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                typ3 = pygame.key.get_pressed()

                if keys[pygame.K_RETURN]:
                    try:
                        pygame.key.set_repeat(0)
                        IPAdress = requests.post("http://127.0.0.1:5000/pHtIv", json= {"hashedKey": serverKey, "pinNo":int(serverPin)}).json()
                        return {
                            "type": "privateJoin",
                            "data": {
                                "IPAddress": IPAdress["IPAddress"],
                                "joinKey": serverKey,
                                "pinNo": serverPin
                            }
                        }
                    except Exception as e:
                        textThree = f"Error: {e}"
        if typ3 is not None:
            collided = pygame.sprite.groupcollide(pointer, textBoxes, False, False)
            for p, t_List in collided.items():
                for tBox in t_List:
                    tBox.typing = True
                    tBox.update(typ3)
                    for textBox in textBoxes.sprites():
                        textBox.typing = False

        f.render_to(screen, (25, 100), textTwo, (0, 0, 0))
        f.render_to(screen, (25, 250), textOne, (0, 0, 0))
        f.render_to(screen, (100, 550), textThree, (0, 0, 0))
        f.render_to(screen, (100,300), textFour, (0, 0, 0))

        f.render_to(screen, (150, 150), serverKey, (0, 0, 0))
        f.render_to(screen, (150, 350), serverPin, (0, 0, 0))

        pointer.update()
        pointer.draw(screen)
        textBoxes.draw(screen)
        pygame.display.update()

'''
Name: characterBuilder
Parameters: screen: object
Returns: character: dictionary
Purpose: Pygame run loop to allow players to design their character
'''
def characterBuilder(screen):
    currSelectedClass = "None Selected"
    currSelectedElement = "None Selected"
    clOne = "Press W for Wizard"
    clTwo = "Press D for Druid"

    elOne = "Press F for Fire"
    elTwo = "Press A for Water"

    finished = "Press Q when you're done creating your character"

    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True

    running = True
    while running:
        screen.fill((255, 255, 255))
        currSelected = 'Selected Class: {selectedClass}   Selected Element: {selectedElement}'.format(selectedClass=currSelectedClass, selectedElement=currSelectedElement)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    currSelectedClass = "Wizard"
                if keys[pygame.K_d]:
                    currSelectedClass = "Druid"
                if keys[pygame.K_a]:
                    currSelectedElement = "Water"
                if keys[pygame.K_f]:
                    currSelectedElement = "Fire"
                if keys[pygame.K_q]:
                    running = False

            f.render_to(screen, (50, 100), currSelected, (0, 0, 0))
            f.render_to(screen, (100, 400), clOne, (0, 0, 0))
            f.render_to(screen, (100, 450), clTwo, (0, 0, 0))
            f.render_to(screen, (100, 550), elOne, (0, 0, 0))
            f.render_to(screen, (100, 600), elTwo, (0, 0, 0))
            f.render_to(screen, (100, 700), finished, (0, 0, 0))
            pygame.display.update()

    character = {
        "caster": currSelectedClass,
        "element": currSelectedElement,
    }
    return character


if __name__ == '__main__':
    pass
