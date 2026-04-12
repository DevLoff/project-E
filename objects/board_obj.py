import pygame

class InputHandler:
    def __init__(self):
        self.inputs = dict()
        self.lag = dict()

    def mod_input(self,tag,num):
        self.inputs[tag] = num
        self.lag[tag] = False

    def pressed(self,tag):
        assert(tag in self.inputs),"Missing input tag"
        if self.test(tag) and not self.lag[tag]:
            return True
        return False

    def test(self,tag):
        if self.inputs[tag]<=0:
            return pygame.mouse.get_pressed()[-self.inputs[tag]]
        return pygame.key.get_pressed()[self.inputs[tag]]

    def update(self):
        for tag in self.lag:
            self.lag[tag] = self.test(tag)

INPUTBOARD = InputHandler()

class SoundHandler:
    def __init__(self):
        self.sounds = dict()

    def mod_sound(self,tag,filepath):
        self.sounds[tag] = pygame.mixer.Sound(filepath)

    def play(self,tag):
        assert (tag in self.sounds),"Missing sound tag"
        self.sounds[tag].play()

SOUNDBOARD = SoundHandler()