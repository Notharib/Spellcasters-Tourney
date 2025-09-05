from characterCreation import Caster

# Spellcaster Classes

'''
Name: Wizard
Purpose: To handle properties of the wizard spellcaster
'''
class Wizard(Caster):
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Wizard object
    '''
    def __init__(self):
        super().__init__()
        self._type = "Wizard"

    '''
    Name: ability
    Parameters: None
    Returns: str
    Purpose: Method for defining the Wizard's ability
    '''
    def ability(self) -> str:
        # Short for extra Damage 
        return "eDam"

    '''
    Name: altAttack
    Parameters: None
    Returns: int
    Purpose: Returns a value that will be assigned to a specific type
    of alternate attack
    '''
    def altAttack(self) -> int:
        # Shotgun style sort of attack
        return 1



'''
Name: Druid
Purpose: To handle properties of the druid spellcaster
'''
class Druid(Caster):
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set the initial values
    of the Druid object
    '''
    def __init__(self):
        super().__init__()
        self._type = "Druid"

    '''
    Name: ability
    Parameters: None
    Returns: str
    Purpose: Getter for the Druid's unique ability
    '''
    def ability(self) -> str:
        # Short for regeneration (will double the Druid's base regeneration)
        return "regen"

    '''
    Name: altAttack
    Parameters: None
    Returns: int
    Purpose: Getter for the value of what the Druid's alternate
    attack is
    '''
    def altAttack(self) -> int:
        # Basic sort of projectile attack 
        return 2
