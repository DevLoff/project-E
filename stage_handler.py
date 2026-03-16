from physic_utils import *

class DisplayHandler:
    def __init__(self, bg):
        self.screen = pygame.display.get_surface()
        self.bg = bg
        self.border = bg.get_rect()
        self.screen.blit(self.bg,(0,0))
        pygame.display.flip()
        self.earlyClears = []
        self.lateClears = []

    def cycle(self):
        pygame.display.update(self.earlyClears + self.lateClears)
        for area in self.earlyClears:
            self.screen.blit(self.bg.subsurface(area.clamp(self.border)), area.topleft)
        self.lateClears = self.earlyClears.copy()
        self.earlyClears.clear()

    def add_area(self, area):
        self.earlyClears.append(area)

    def dynamic_blit(self, surface, dest):
        self.add_area(self.screen.blit(surface, dest))