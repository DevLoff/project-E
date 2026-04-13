import pygame
from objects.visual_obj import UIItem
from objects.board_obj import INPUTBOARD, SOUNDBOARD
from objects.level_obj import Stage
from utils.menu_util import switch_stage, stop

class Button(UIItem):
    def __init__(self,rect,img,action,target):
        super().__init__(rect,img)
        self.parent = None
        self.effect = action
        self.target = target

    def execute(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            SOUNDBOARD.play("click")
            if self.effect == "switch":
                switch_stage(self.parent.handling,self.target)
            elif self.effect == "exit":
                stop(self.parent.handling)

class Menu(Stage):
    def __init__(self):
        super().__init__()
        # INTERACTIBLE
        self.labels = []
        self.buttons = []
        self.sliders = []
        self.rolls = []
        # LAYERS
        size = pygame.display.get_surface().get_size()
        self.bgLayer = pygame.Surface(size)
        self.uiLayer = pygame.Surface(size, flags=pygame.SRCALPHA)
        # RENDER MEM
        self.toCleanRects = []

    def add_label(self,label):
        self.labels.append(label)
    def add_button(self,button):
        button.parent = self
        self.buttons.append(button)

    def update(self,**info):
        for button in self.buttons:
            if INPUTBOARD.pressed("click"):
                button.execute()

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
            newRects.append(self.uiLayer.blit(item.img,item.rect.topleft))
        return newRects

    def render(self):
        window = pygame.display.get_surface()
        newRects = []
        window.blit(self.bgLayer, (0, 0))
        newRects += self.set_uilayer()
        window.blit(self.uiLayer, (0, 0))
        pygame.display.flip()
        self.toCleanRects = newRects