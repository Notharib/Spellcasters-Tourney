import pygame, pygame.freetype, socket

class TextBox(pygame.sprite.Sprite):
    def __init__(self, position, typing=False):
        super().__init__()
        self.X = position[0]
        self.Y = position[1]
        self.height = 30
        self.width = 50
        self.colour = (200,200,200)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image, self.colour, (self.X, self.Y, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y
        self.typing = typing

    def update(self):
        if self.typing:
            pass

class Pointer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.X = pygame.mouse.get_pos()[0]
        self.Y = pygame.mouse.get_pos()[1]
        self.height = 1
        self.width = 1
        self.colour =  (255,255,255)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image, self.colour, (self.X, self.Y, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y

    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.rect.x = mousePos[0]
        self.rect.y = mousePos[1]

def gameStart(screen):
    running = True
    textOne = "Welcome to Wizards Tourney. These are your options for playing:"
    textTwo = "1) Press P to join the public server"
    textThree = "2) Press A to create a private server"

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
                        running = False
                    elif keys[pygame.K_a]:
                         g = privateGame(screen)
                         return g

            f.render_to(screen,(100,400),textOne, (0,0,0))
            f.render_to(screen, (100, 500), textTwo, (0, 0, 0))
            f.render_to(screen, (100, 550), textThree, (0, 0, 0))
            pygame.display.update()
        return True

def privateGame(screen):
    noOfPlayers = "EXAMPLE"
    textOne = "Enter number of players you wish to be able to join the private server: "

    gameLength = "EXAMPLE"
    textTwo = "Enter the amount of time you wish to have the game go on for: "

    textThree = "Press ENTER when you wish to wait for players to start joining"

    f = pygame.freetype.SysFont("Comic Sans MS", 24)
    f.origin = True

    pointer = pygame.sprite.Group()
    textBoxes = pygame.sprite.Group()

    pointer.add(Pointer())

    running = True
    while running:
        screen.fill((255, 255, 255))

        for textBox in textBoxes:
            textBox.typing = False

        for event in pygame.event.get():
            if event == pygame.QUIT:
                return False

            if event == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

                collided = pygame.sprite.groupcollide(pointer,textBoxes,False,False)
                for p, t_List in collided.items():
                    for tBox in t_List:
                        tBox.update()

        f.render_to(screen,(100,400),textOne, (0,0,0))
        f.render_to(screen, (150,400), noOfPlayers, (0, 0, 0))
        f.render_to(screen, (100, 500), textTwo, (0, 0, 0))
        f.render_to(screen, (100, 550), gameLength, (0, 0, 0))
        f.render_to(screen, (100, 650), textThree, (0, 0, 0))

        pointer.update()
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