import pygame
from objects.board_obj import INPUTBOARD, FONTBOARD
from objects.visual_obj import UIItem

import random

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
        self.raindrops = []
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
        self.rain_triggered = False
        self.next_level_json = None
        # MEMORY
        self.toCleanRects = []
        self.root = ori
        # DEBUG
        self.debugLayer = pygame.Surface(size,flags=pygame.SRCALPHA)
        self.debugMode = True
        print("LEVEL CREATED")


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
            for cloud in self.clouds:
                if not self.rain_triggered and peg.pos.distance_to(cloud.pos) < 50:
                    for i in range(25):
                        spawn_x = cloud.pos[0] + random.randint(-40, 40)
                        spawn_y = cloud.pos[1] + 21
                        self.raindrops.append(Droplet(spawn_x, spawn_y))
                    self.rain_triggered = True
                    self.pegs.remove(peg)
                    self.launched = False
                    return 2

            if peg.move_and_slide(dt,self.gravity,self.platforms):
                for field in self.fields:
                    field.update(peg)
            if not pygame.display.get_surface().get_rect().collidepoint(peg.pos):
                self.pegs.remove(peg)
        if INPUTBOARD.pressed("reset"):
            self.pegs.clear()
        if len(self.pegs) < 1:
            self.rain_triggered = False
            self.launched = False
            self.rack_peg()
            return 2

        return 3

    def tactic(self):
        if len(self.pegs) > 0:
            self.pegs[0].pos = self.ports[self.initial].pos.copy()

            # Add a small check: Only launch if the mouse was NOT just used for a menu
            if INPUTBOARD.pressed("launch"):
                # Clear the input so it doesn't trigger twice
                INPUTBOARD.inputs["launch"] = False
                self.launched = True
                self.launch_peg()
        else:
            self.rack_peg()

    def update(self,**info):
        for drop in self.raindrops:
            drop.update()
        self.raindrops = [d for d in self.raindrops if d.active]

        if self.feasibility():
            if self.launched:
                return self.simulate(info["dt"])
            else:
                self.tactic()
                return 2
        else:
            self.wincondition()
            return 1

    def construct_endui(self):
        score = str(sum([field.score for field in self.fields]))
        self.handling.add_data("score",score)
        item = pygame.Surface((300,200))
        item.blit(FONTBOARD.render(score, "arial", 30),(0, 30))
        return item

    def wincondition(self):
        # 1. Use 'loadedStage' because your Game class uses that for the loop
        if not self.handling:
            return

        # Check if we are already transitioning to avoid the infinite loop
        # We check both current_stage and loadedStage to be safe
        if hasattr(self.handling, 'loadedStage'):
            if self.handling.loadedStage != self:
                return

        if INPUTBOARD.pressed("click"):
            INPUTBOARD.inputs["click"] = False

            try:
                import level_handler
                target = self.next_level_json if self.next_level_json else "stages/levels/level02.json"

                # Use the 'time gate' logic in level_handler to stop the multiple loads
                next_lvl = level_handler.load_level(target, self.root)

                if next_lvl:
                    # 2. Tell the Game object to switch to Level 2
                    next_lvl.handling = self.handling
                    self.handling.loadedStage = next_lvl

                    # Also set current_stage if the Game class uses it
                    if hasattr(self.handling, 'current_stage'):
                        self.handling.current_stage = next_lvl

                    # 3. Setup Level 2 visual
                    next_lvl.debugMode = False
                    next_lvl.set_staticlayers(pygame.image.load("Images/newyork1a.png"))

                    # 4. Force one clean frame of Level 2
                    next_lvl.render()

                    print("SUCCESS: Transitioned to Level 2.")
                    return
            except Exception as e:
                print(f"Transition Error: {e}")


    def set_staticlayers(self, bg):
        # FORCE a brand new surface for the new level
        size = pygame.display.get_surface().get_size()
        self.bgLayer = pygame.Surface(size).convert()

        # If bg is a string (path), load it. If it's a surface, blit it.
        if isinstance(bg, str):
            bg_img = pygame.image.load(bg).convert()
            self.bgLayer.blit(pygame.transform.scale(bg_img, size), (0, 0))
        else:
            self.bgLayer.blit(pygame.transform.scale(bg, size), (0, 0))

        # Add ports and clouds
        for port in self.ports:
            self.bgLayer.blit(port.img, port.pos + port.offset)
        for cloud in self.clouds:
            self.bgLayer.blit(cloud.img, cloud.pos + cloud.offset)

    def cover(self):
        window = pygame.display.get_surface()
        window.blit(self.bgLayer, (0, 0))
        window.blit(self.debugLayer, (0, 0))
        pygame.display.flip()

    def set_activelayer(self,win):
        newRects = []
        for drop in self.raindrops:
            drop.draw(win)
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
        if window is None: return

        # 1. Background (The baked layer with clouds)
        window.blit(self.bgLayer, (0, 0))

        # 2. Objects (The seeds and rain)
        self.set_activelayer(window)

        # 3. UI (The bench of seeds at the bottom)
        self.set_uilayer(window)

        # 4. Only show debug shapes if debugMode is True
        if self.debugMode:
            window.blit(self.debugLayer, (0, 0))

        # 5. The ONLY flip
        pygame.display.flip()

class Droplet:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.speed = random.uniform(7, 12)
        self.length = random.randint(4, 8)
        self.active = True

    def update(self):
        self.pos[1] += self.speed
        if self.pos[1] > 580:
            self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.line(screen, (160, 210, 255), (self.pos[0], self.pos[1]),
                             (self.pos[0], self.pos[1] + self.length), 1)
            pygame.draw.line(screen, (200, 240, 255), (self.pos[0], self.pos[1]), (self.pos[0], self.pos[1] + 2), 1)