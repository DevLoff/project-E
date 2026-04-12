import pygame
from objects.visual_obj import UIItem
from objects.input_obj import INPUTBOARD
from objects.level_obj import Stage

class Action:
    def __init__(self,t,**opts):
        self.type = t
        self.options = opts

    def execute(self):
        if self.type == "toggle":
            self.fct_toggle()

    def fct_toggle(self):
        if "target" in self.options:
            self.options["target"].visibility = not self.options["target"].visibility

class Button(UIItem):
    def __init__(self,rect,img,action):
        super().__init__(rect,img)
        self.effect = action

class Menu(Stage):
    def __init__(self):
        super().__init__()
        # INTERACTIBLE
        self.labels = []
        self.buttons = []
        self.sliders = []
        self.rolls = []
        # LAYERS
        self.bgLayer = pygame.Surface((0,0))
        self.uiLayer = pygame.Surface((0,0), flags=pygame.SRCALPHA)
        # RENDER MEM
        self.toCleanRects = []

    def update(self,**info):
        for button in self.buttons:
            if INPUTBOARD.pressed("click") and button.visibility:
                button.action.execute()

    def set_staticlayers(self,bg):
        self.bgLayer.blit(bg, (0, 0))
        self.cover()

    def cover(self):
        window = pygame.display.get_surface()
        window.blit(self.bgLayer, (0, 0))
        pygame.display.flip()

    def set_uilayer(self):
        self.uiLayer = pygame.Surface(self.bgLayer.get_size(), flags=pygame.SRCALPHA)
        newRects = []
        for item in self.labels+self.buttons+self.sliders+self.rolls:
            if item.visibility:
                newRects.append(self.uiLayer.blit(item.img,item.rect.topleft))
        return newRects

    def render(self):
        window = pygame.display.get_surface()
        newRects = []
        window.blit(self.bgLayer, (0, 0))
        newRects += self.set_uilayer()
        window.blit(self.uiLayer, (0, 0))
        pygame.display.update(newRects + self.toCleanRects)
        self.toCleanRects = newRects