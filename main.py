# IMPORT

from level_handler import *
from stage_handler import *

"""
CONSTANT_CONSTANT : use upper case
variableVariable : use camel case
argumentargument : use lower case
function_function : use snake case
"""

class DisplayHandler:
    def __init__(self, surface):
        self.surface = surface
        self.current_stage = None # The loop looks at this
        self.data = {}

    def load_stage(self, stage):
        self.current_stage = stage
        if self.current_stage:
            self.current_stage.handling = self
            self.current_stage.cover()
            print("Handler updated: Level Changed Successfully.")

    def add_data(self, key, value):
        self.data[key] = value


def launch_new_game(tracker, display_handler, level_path, menu_root):
    new_lvl = load_level(level_path, menu_root)
    if new_lvl:
        new_lvl.handling = display_handler
        display_handler.load_stage(new_lvl)
        new_lvl.debugMode = True
        tracker[0] = 2

def enlarge_range(origin,new):
    return [min(origin[0],new[0]),max(origin[1],new[1])]
def intersect(l1,l2):
    return (l1[0]<l2[1])==(l2[0]<l1[1])



if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    # CONSTANTS
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    STATIC_BG = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()
    GAMEFONT = pygame.font.SysFont("comicsansms",20)

    # META SETUP
    pygame.display.set_caption("Tears of Sky")
    pygame.display.set_icon(pygame.image.load("Images/logo.png"))

    # VARIABLES
    gameStageTracker = [1] # 0:game ended, 1:game running, 2:level running, 3:peg launched
    eventList : list
    dt : float
    MENU_BG = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    MENU_BG.fill((255, 255, 255))
    menuDisplay = DisplayHandler(MENU_BG)
                   (0, 0))
    levelDisplay = DisplayHandler(STATIC_BG)

    # MENU
    boxAspect = pygame.image.load("Images/no_tex.png").convert_alpha()

    buttons = [
        Button(pygame.Rect(330, 275, 240, 60), boxAspect,
               lambda x: launch_new_game(gameStageTracker, levelDisplay, "stages/levels/level01.json", menuDisplay),
               True),

        Button(pygame.Rect(330, 365, 240, 60), boxAspect,
               lambda x: launch_new_game(gameStageTracker, levelDisplay, "stages/levels/level02.json", menuDisplay),
               True),

        # EXIT BUTTON (Bottom one)
        Button(pygame.Rect(330, 455, 240, 60), boxAspect,
               lambda x: quit(),
               True),
    ]
    level = None


    menuDisplay.cover()

# --- SOUND INITIALIZATION ---
    pygame.mixer.init()
    pygame.mixer.music.load("Sound/Street Party.mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)

    rain_sound = pygame.mixer.Sound("Sound/rain_v1.wav")
    rain_sound.set_volume(1.0)
    while gameStageTracker[0] > 0:
        dt = CLOCK.tick(60) / 1000
        eventList = pygame.event.get()

        for evnt in eventList:
            if evnt.type == pygame.QUIT:
                gameStageTracker[0] = 0


            if gameStageTracker[0] == 1:
                if evnt.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        button.update(evnt.pos, buttons)
        active_stage = levelDisplay.current_stage

        if gameStageTracker[0] >= 2 and active_stage is not None:
            if hasattr(active_stage, 'is_raining') and active_stage.is_raining:
                if not pygame.mixer.get_busy():
                    rain_sound.play(loops=-1)
            else:
                rain_sound.stop()
            gameStageTracker[0] = active_stage.update(dt=dt)
            active_stage = levelDisplay.current_stage
            SCREEN.fill((0, 0, 0))
            active_stage.render()
            SCREEN.blit(levelDisplay.surface, (0, 0))
        else:
            SCREEN.fill((255, 255, 255))
            for button in buttons:
                button.render(SCREEN)

        pygame.display.flip()
