import pygame
import pygame.freetype
import requests

from time import sleep

from colours import Colours

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
    textFour = ""

    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True


    while running:

        while running:
            screen.fill(Colours.WHITE.value)
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

            f.render_to(screen,(50,300),textOne, Colours.BLACK.value)
            f.render_to(screen, (100, 400), textTwo, Colours.BLACK.value)
            f.render_to(screen, (100, 550), textFour, Colours.BLACK.value)
            pygame.display.update()
        return True

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
    elThree = "Press E for Earth"

    finished = "Press Q when you're done creating your character"

    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True

    running = True
    while running:
        screen.fill(Colours.WHITE.value)
        currSelected = f'Selected Class: {currSelectedClass}   Selected Element: {currSelectedElement}'

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
                if keys[pygame.K_e]:
                    currSelectedElement = "Earth"
                if keys[pygame.K_q]:
                    running = False

            f.render_to(screen, (50, 100), currSelected, Colours.BLACK.value)
            f.render_to(screen, (100, 400), clOne, Colours.BLACK.value)
            f.render_to(screen, (100, 450), clTwo, Colours.BLACK.value)
            f.render_to(screen, (100, 550), elOne, Colours.BLACK.value)
            f.render_to(screen, (100, 600), elTwo, Colours.BLACK.value)
            f.render_to(screen, (100, 650), elThree, Colours.BLACK.value)
            f.render_to(screen, (100, 700), finished, Colours.BLACK.value)
            pygame.display.update()

    character = {
        "caster": currSelectedClass,
        "element": currSelectedElement,
    }
    return character