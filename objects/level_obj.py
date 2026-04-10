import pygame

class Level:
    def __init__(self):
        # PHYSIC OBJECTS
        self.platforms = []
        self.clouds = []
        self.bench = []
        self.pegs = []
        self.ports = []
        self.fields = []
        # LAYERS
        size = pygame.display.get_surface().get_size()
        self.bgLayer = pygame.Surface(size)
        self.activeLayer = pygame.Surface(size,flags=pygame.SRCALPHA)
        self.frontLayer = pygame.Surface(size,flags=pygame.SRCALPHA)
        self.uiLayer = pygame.Surface(size,flags=pygame.SRCALPHA)
        # PARAMETER
        self.gravity = pygame.Vector2(0,100)
        self.airres = 0
        self.throw = 1
        self.initial = 0
        self.launched = False
        # RENDER MEM
        self.toCleanRects = []
        # DEBUG
        self.debugLayer = pygame.Surface(size,flags=pygame.SRCALPHA)
        self.debugMode = True

    def feasibility(self):
        return len(self.bench+self.pegs)>0

    def initialize_pegs(self,*pegs):
        for peg in pegs:
            self.bench.append(peg)
        self.rack_peg()

    def initialize_cloud(self,*clouds):
        for cloud in clouds:
            self.clouds.append(cloud)
            self.platforms += cloud.hitboxes

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
            peg.move_and_slide(dt,self.gravity,self.platforms)
            if not pygame.display.get_surface().get_rect().collidepoint(peg.pos):
                self.pegs.remove(peg)
        if len(self.pegs) < 1:
            self.launched = False
            self.rack_peg()
    def tactic(self):
        self.pegs[0].pos = self.ports[self.initial].pos.copy()
        if pygame.mouse.get_pressed()[0]:
            self.launched = True
            self.launch_peg()

    def update(self,dt):
        if self.launched:
            self.simulate(dt)
        else:
            self.tactic()

    def set_staticlayers(self,bg):
        window = pygame.display.get_surface()
        self.bgLayer.blit(bg,(0,0))
        for port in self.ports:
            self.bgLayer.blit(port.img,port.pos+port.offset)
        for cloud in self.clouds:
            self.frontLayer.blit(cloud.img, cloud.pos + cloud.offset)
        window.blit(self.bgLayer, (0, 0))
        window.blit(self.frontLayer, (0, 0))
        if self.debugMode:
            for platform in self.platforms:
                platform.hitbox(self.debugLayer)
            window.blit(self.debugLayer, (0, 0))
        pygame.display.flip()

    def set_activelayer(self):
        self.activeLayer = pygame.Surface(self.bgLayer.get_size(),flags=pygame.SRCALPHA)
        newRects = []
        for field in self.fields:
            newRects.append(self.activeLayer.blit(field.img,field.pos+field.offset))
        for peg in self.pegs:
            newRects.append(self.activeLayer.blit(peg.img,peg.pos+peg.offset))
        return newRects

    def set_uilayer(self):
        self.uiLayer = pygame.Surface(self.bgLayer.get_size(), flags=pygame.SRCALPHA)
        newRects = []
        for peg in self.bench:
            newRects.append(self.uiLayer.blit(peg.img,peg.pos+peg.offset))
        return newRects

    def render(self):
        window = pygame.display.get_surface()
        newRects = []
        window.blit(self.bgLayer, (0, 0))
        newRects += self.set_activelayer()
        window.blit(self.activeLayer, (0, 0))
        window.blit(self.frontLayer, (0, 0))
        newRects += self.set_uilayer()
        window.blit(self.uiLayer, (0, 0))
        window.blit(self.debugLayer, (0, 0))
        pygame.display.flip()
        self.toCleanRects = newRects
