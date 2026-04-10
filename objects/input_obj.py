import pygame

class InputHandler:
    def __init__(self):
        self.inputs = dict()

    def mod_input(self,tag,num):
        self.inputs[tag] = num

    def pressed(self,tag):
        assert(tag in self.inputs),"Missing input tag"
        if self.inputs[tag]<=0:
            return pygame.mouse.get_pressed()[-self.inputs[tag]]
        return pygame.key.get_pressed()[self.inputs[tag]]

INPUTBOARD = InputHandler()