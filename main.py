# IMPORT
from pygame import *

"""
CONSTANT_CONSTANT : use upper case
variableVariable : use camel case
argumentargument : use lower case
function_function : use snake case
"""

if __name__ == '__main__':
    init()

    # CONSTANTS
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SCREEN = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # VARIABLES
    isGameRunning = True
    eventList : list

    # GAME LOOP
    while isGameRunning:
        # EVENT HANDLER
        eventList = event.get()

        # TEMPORARY SYSTEM
        for evnt in eventList:
            if evnt.type == QUIT:
                isGameRunning = False

    quit()