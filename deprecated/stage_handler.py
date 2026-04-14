from deprecated.physic_utils import *
import pickle
from level_handler import Peg

class DisplayHandler:
    def __init__(self, bg):
        self.screen = pygame.display.get_surface()
        self.bg = bg
        self.border = bg.get_rect()
        self.screen.blit(self.bg,(0,0))
        pygame.display.flip()
        self.earlyClears = []
        self.lateClears = []

    def cover(self):
        self.screen.blit(self.bg, (0, 0))
        pygame.display.flip()

    def cycle(self):
        pygame.display.update(self.earlyClears + self.lateClears)
        for area in self.earlyClears:
            self.screen.blit(self.bg.subsurface(area.clamp(self.border)), area.topleft)
        self.lateClears = self.earlyClears.copy()
        self.earlyClears.clear()

    def add_area(self, area):
        if type(area) == pygame.Rect:
            self.earlyClears.append(area)
        if type(area) == list:
            self.earlyClears += area

    def object_blit(self,obj):
        self.add_area(obj.render(self.screen))
    def dynamic_blit(self, surface, dest):
        self.add_area(self.screen.blit(surface, dest))

class Button:
    def __init__(self, rect, aspect, action, visibility):
        self.rect = rect
        self.image = pygame.transform.scale(aspect, rect.size)
        self.action = action
        self.visibility = visibility

    def update(self, mousepos, *args):
        if self.rect.collidepoint(mousepos) and self.visibility:
            self.action(args)

    def render(self, surface):
        if self.visibility:
            return surface.blit(self.image, self.rect.topleft)
        return None

def narrow_visible(ext, *ks):
    for i in range(len(ext[0])):
        ext[0][i].visibility = False
    for k in ks:
        if -1 < k < len(ext[0]):
            ext[0][k].visibility = True

def launch_level(ext,loader):
    ext[2].cover()
    newLvl = pickle.load(open(loader,"rb"))
    ext[3].__init__()
    ext[3].platforms = newLvl
    ext[3].bench.append(Peg(10, pygame.image.load("../Images/pegs/peg.png")))
    ext[3].rack_peg()
    ext[1][0] = 2