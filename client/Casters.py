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
