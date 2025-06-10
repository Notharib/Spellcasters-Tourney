import pygame

'''
Name: TextBox
Inherits: pygame.sprite.Sprite
Purpose: To create a textbox that players need to move their pointer over in
order to be able to type
'''
class TextBox(pygame.sprite.Sprite):
    '''
    Name: __init__
    Parameters: position: array, text:string, allow:string, typing:boolean
    Returns: None
    Purpose: Constructor to set the initial values
    of the TextBox object
    '''
    def __init__(self, position, text, allow="allInput",  typing=False):
        super().__init__()
        self.X = position[0]
        self.Y = position[1]
        self.height = 30
        self.width = 50
        self.colour = (200,0,0)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)
        pygame.draw.rect(self.image, self.colour, (self.X, self.Y, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y
        self.typing = typing
        self.text = text
        self.allow = allow

    '''
    Name: checkIfExample
    Parameters: None
    Returns: boolean
    Purpose: Checks whether the value held in self.text is EXAMPLE or if it something else, and
    returns the corresponding boolean value
    '''
    def checkIfExample(self):
        if self.text == "EXAMPLE":
            return True
        else:
            return False

    '''
    Name: update
    Parameters: keys:list
    Returns: None
    Purpose: Updates the value of self.text based upon what key the player is pressing
    '''
    def update(self, keys):
        if self.typing:
            alphabetToPygame = {
                "a": pygame.K_a,
                "b": pygame.K_b,
                "c": pygame.K_c,
                "d": pygame.K_d,
                "e": pygame.K_e,
                "f": pygame.K_f,
                "g": pygame.K_g,
                "h": pygame.K_h,
                "i": pygame.K_i,
                "j": pygame.K_j,
                "k": pygame.K_k,
                "l": pygame.K_l,
                "m": pygame.K_m,
                "n": pygame.K_n,
                "o": pygame.K_o,
                "p": pygame.K_p,
                "q": pygame.K_q,
                "r": pygame.K_r,
                "s": pygame.K_s,
                "t": pygame.K_t,
                "u": pygame.K_u,
                "v": pygame.K_v,
                "w": pygame.K_w,
                "x": pygame.K_x,
                "y": pygame.K_y,
                "z": pygame.K_z
            }

            if self.allow == "allInput" or self.allow == "numberInput":
                if keys[pygame.K_1]:
                    if not self.checkIfExample():
                        self.text += "1"
                    else:
                        self.text = "1"
                elif keys[pygame.K_2]:
                    if not self.checkIfExample():
                        self.text += "2"
                    else:
                        self.text = "2"
                elif keys[pygame.K_3]:
                    if not self.checkIfExample():
                        self.text += "3"
                    else:
                        self.text = "3"
                elif keys[pygame.K_4]:
                    if not self.checkIfExample():
                        self.text += "4"
                    else:
                        self.text = "4"
                elif keys[pygame.K_5]:
                    if not self.checkIfExample():
                        self.text += "5"
                    else:
                        self.text = "5"
                elif keys[pygame.K_6]:
                    if not self.checkIfExample():
                        self.text += "6"
                    else:
                        self.text = "6"
                elif keys[pygame.K_7]:
                    if not self.checkIfExample():
                        self.text += "7"
                    else:
                        self.text = "7"
                elif keys[pygame.K_8]:
                    if not self.checkIfExample():
                        self.text += "8"
                    else:
                        self.text = "8"
                elif keys[pygame.K_9]:
                    if not self.checkIfExample():
                        self.text += "9"
                    else:
                        self.text = "9"
                elif keys[pygame.K_0]:
                    if not self.checkIfExample():
                        self.text += "0"
                    else:
                        self.text = "0"
                elif keys[pygame.K_BACKSPACE]:
                    if self.checkIfExample():
                        self.text = ""
                    else:
                        self.text = self.text[:-1]
            if self.allow == "allInput" or self.allow == "textInput":
                mods = pygame.key.get_mods()
                for letter in list(alphabetToPygame.keys()):
                    if keys[alphabetToPygame[letter]] and mods != 0:
                        if not self.checkIfExample():
                            self.text += letter.upper()
                        else:
                            self.text = letter.upper()
                    elif keys[alphabetToPygame[letter]]:
                        if not self.checkIfExample():
                            self.text += letter
                        else:
                            self.text = letter
                if keys[pygame.K_BACKSPACE]:
                    if self.checkIfExample():
                        self.text = ""
                    else:
                        self.text = self.text[:-1]



'''
Name: Pointer
Inherits: pygame.sprite.Sprite
Purpose: To have an object that follows the player's cursor so that it can interact with textboxes
'''
class Pointer(pygame.sprite.Sprite):
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Pointer object
    '''
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

    '''
    Name: update
    Parameters: None
    Returns: None
    Purpose: Updates the rect position of the Pointer object based
    upon the location of the cursor
    '''
    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.rect.x = mousePos[0]
        self.rect.y = mousePos[1]