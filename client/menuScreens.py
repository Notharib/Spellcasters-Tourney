import pygame, pygame.freetype, requests, socket
from gameLogic import TextBox, Pointer, Fire, Water, Wizard, Druid

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
        type = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                print("EVENT KEY PRESSED!!!!")
                keys = pygame.key.get_pressed()
                type = pygame.key.get_pressed()
                if keys[pygame.K_l]:
                    print("Private Game Made!")
                    pygame.key.set_repeat(0)
                    joinKey = requests.post("http://127.0.0.1:5000/pItHv", json={"IPAddress":socket.gethostbyname(socket.gethostname())}).json()["hashedItem"]
                    return {
                        "type": "privateCreate",
                        "data": {
                            "lengthOfGame": gameLength,
                            "noOfPlayers": noOfPlayers,
                            "joinKey": joinKey
                        }
                    }
            # if event.type == pygame.KEYUP:
            #     type = pygame.key.get_pressed()

        if type is not None:
            collided = pygame.sprite.groupcollide(pointer, textBoxes, False, False)
            for p, t_List in collided.items():
                for tBox in t_List:
                    tBox.typing = True
                    tBox.update(type)
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

def enterPrivGameInfo(screen):
    textOne = "Press ENTER to join the server!"
    textTwo = "Server Key: "
    textThree = ""
    serverKey = ""

    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True

    pointer = pygame.sprite.Group()
    textBoxes = pygame.sprite.Group()

    pointer.add(Pointer())

    textBoxes.add(TextBox(position=(150, 150), text=serverKey))

    running = True
    while running:
        screen.fill((255, 255, 255))

        serverKey = textBoxes.sprites()[0].text

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event == pygame.QUIT:
                return None
            if event == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_RETURN]:
                    try:
                        return {
                            "type": "privateJoin",
                            "data": {
                                "IPAddress": requests.post("http://127.0.0.1:5000/pHtIv", json= {"hashedKey": serverKey})["IPAddress"],
                                "joinKey": serverKey
                            }
                        }
                    except Exception as e:
                        textThree = f"Error: {e}"

        collided = pygame.sprite.groupcollide(pointer, textBoxes, False, False)
        for p, t_List in collided.items():
            for tBox in t_List:
                tBox.typing = True
                tBox.update(keys)
                for textBox in textBoxes.sprites():
                    textBox.typing = False

        f.render_to(screen, (25, 100), textTwo, (0, 0, 0))
        f.render_to(screen, (150, 150),serverKey , (0, 0, 0))
        f.render_to(screen, (25, 250), textOne, (0, 0, 0))
        f.render_to(screen, (100, 550), textThree, (0, 0, 0))

        pointer.update()
        pointer.draw(screen)
        textBoxes.draw(screen)
        pygame.display.update()


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
        "spellcastingType": currSelectedClass,
        "element": currSelectedElement,
    }
    return character


if __name__ == '__main__':
    pass