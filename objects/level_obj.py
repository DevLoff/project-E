import pygame
from objects.board_obj import INPUTBOARD, FONTBOARD
from objects.visual_obj import UIItem


class Stage:
    def __init__(self):
        self.handling = None
    def cover(self):
        pass
    def update(self,**info):
        pass
    def render(self):
        pass

class Level(Stage):
    def __init__(self,ori = None):
        super().__init__()
        # OBJECTS
        self.platforms = []
        self.clouds = []
        self.bench = []
        self.pegs = []
        self.ports = []
        self.fields = []
        self.hud = dict()
        # LAYERS
        size = pygame.display.get_surface().get_size()
        self.bgLayer = pygame.Surface(size)
        # PARAMETER
        self.gravity = pygame.Vector2(0,100)
        self.airres = 0
        self.throw = 1
        self.initial = 0
        self.launched = False
        # MEMORY
        self.toCleanRects = []
        self.root = ori
        # DEBUG
        self.debugLayer = pygame.Surface(size,flags=pygame.SRCALPHA)
        self.debugMode = True

    def feasibility(self):
        return len(self.bench+self.pegs)>0

    def add_port(self,port):
        self.ports.append(port)
    def add_peg(self,peg):
        self.bench.append(peg)
    def add_cloud(self,cloud):
        self.clouds.append(cloud)
        self.platforms += cloud.hitboxes
    def add_field(self,field):
        self.fields.append(field)

    def rack_peg(self):
        if len(self.bench)>0:
            self.pegs.append(self.bench.pop())
    def launch_peg(self):
        modality = self.get_launch_parameter()
        self.pegs[0].velocity += modality[0]*modality[1]*self.throw
    def get_launch_parameter(self):
        inputVec = pygame.Vector2(pygame.mouse.get_pos()) -  self.ports[self.initial].pos
        return inputVec.length(),inputVec.normalize()

    def arrange_bench(self,initalpos,delta):
        start,move = pygame.Vector2(initalpos),pygame.Vector2(delta)
        for i in range(len(self.bench)):
            self.bench[i].pos = start+move*i

    def simulate(self,dt):
        for peg in self.pegs:
            if peg.move_and_slide(dt,self.gravity,self.platforms):
                for field in self.fields:
                    field.update(peg)
            if not pygame.display.get_surface().get_rect().collidepoint(peg.pos):
                self.pegs.remove(peg)
        if INPUTBOARD.pressed("reset"):
            self.pegs.clear()
        if len(self.pegs) < 1:
            self.launched = False
            self.rack_peg()

    def tactic(self):
        self.pegs[0].pos = self.ports[self.initial].pos.copy()
        if INPUTBOARD.pressed("launch"):
            self.launched = True
            self.launch_peg()

    def update(self,**info):
        if self.feasibility():
            if self.launched:
                self.simulate(info["dt"])
            else:
                self.tactic()
        else:
            self.wincondition()

    def construct_endui(self):
        score = str(sum([field.score for field in self.fields]))
        self.handling.add_data("score",score)
        item = pygame.Surface((300,200))
        item.blit(FONTBOARD.render(score, "arial", 30),(0, 30))
        return item

    def wincondition(self):
        if "endui" not in self.hud:
            self.hud["endui"] = UIItem(pygame.Rect(0,0,300,200),None)
            self.hud["endui"].raw_image(self.construct_endui())
        if INPUTBOARD.pressed("click"):
            if self.root is not None:
                self.handling.load_stage(self.root)
            else:
                quit()

    def set_staticlayers(self,bg):
        self.bgLayer.blit(bg,(0,0))
        for port in self.ports:
            self.bgLayer.blit(port.img,port.pos+port.offset)
        for cloud in self.clouds:
            self.bgLayer.blit(cloud.img, cloud.pos + cloud.offset)
        if self.debugMode:
            for platform in self.platforms:
                platform.hitbox(self.debugLayer)
        self.cover()

    def cover(self):
        window = pygame.display.get_surface()
        window.blit(self.bgLayer, (0, 0))
        window.blit(self.debugLayer, (0, 0))
        pygame.display.flip()

    def set_activelayer(self,win):
        newRects = []
        for field in self.fields:
            newRects.append(win.blit(field.img,field.pos+field.offset))
        for peg in self.pegs:
            newRects.append(win.blit(peg.img,peg.pos+peg.offset))
        return newRects

    def set_uilayer(self,win):
        newRects = []
        for item in self.hud:
            newRects.append(win.blit(self.hud[item].img, self.hud[item].rect.topleft))
        for peg in self.bench:
            newRects.append(win.blit(peg.img,peg.pos+peg.offset))
        return newRects

    def render(self):
        window = pygame.display.get_surface()
        newRects = []
        newRects += self.set_activelayer(window)
        newRects += self.set_uilayer(window)
        for rect in newRects:
            window.blit(self.debugLayer.subsurface(rect), rect.topleft)
        pygame.display.flip()
        for rect in newRects:
            window.blit(self.bgLayer.subsurface(rect), rect.topleft)
            window.blit(self.debugLayer.subsurface(rect), rect.topleft)