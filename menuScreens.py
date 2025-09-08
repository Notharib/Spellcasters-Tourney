import socket

from time import sleep
import pygame
import pygame.freetype
import requests
from menuClasses import Pointer, TextBox

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
            f.render_to(screen, (100, 550), textFour, (0, 0, 0))
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
                if keys[pygame.K_e]:
                    currSelectedElement = "Earth"
                if keys[pygame.K_q]:
                    running = False

            f.render_to(screen, (50, 100), currSelected, (0, 0, 0))
            f.render_to(screen, (100, 400), clOne, (0, 0, 0))
            f.render_to(screen, (100, 450), clTwo, (0, 0, 0))
            f.render_to(screen, (100, 550), elOne, (0, 0, 0))
            f.render_to(screen, (100, 600), elTwo, (0, 0, 0))
            f.render_to(screen, (100, 650), elThree, (0, 0, 0))
            f.render_to(screen, (100, 700), finished, (0, 0, 0))
            pygame.display.update()

    character = {
        "caster": currSelectedClass,
        "element": currSelectedElement,
    }
    return character


if __name__ == '__main__':
    pass
