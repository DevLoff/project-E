import pygame

pygame.init()

def gradiant(surface,rx=1,ry=1):
    return surface.subsurface(pygame.Rect(0,0,surface.get_width()*rx,surface.get_height()*ry))

class Button:
    def __init__(self,rect,aspect,action,visibility):
        self.rect = rect
        self.image = pygame.transform.scale(aspect,rect.size)
        self.action = action
        self.visibility = visibility
    def update(self,mousepos,*args):
        if self.rect.collidepoint(mousepos) and self.visibility:
            print("BUTTON CLICKED")
            self.action(args)
    def render(self,surface):
        if self.visibility:
            return surface.blit(self.image,self.rect.topleft)
        return None

def narrow_visible(displayed,*ks):
    for i in range(len(displayed)):
        displayed[i].visibility = False
    for k in ks:
        if -1<k<len(displayed):
            displayed[k].visibility = True

SCREEN = pygame.display.set_mode((800,600))
bgColor = pygame.Color(255,255,255)

boxAspect = pygame.image.load("Images/no_tex.png").convert_alpha()

buttons = [
    Button(pygame.Rect(100,100,100,50),boxAspect,lambda x: narrow_visible(x[0],1,0),True),
    Button(pygame.Rect(300,100,100,50),boxAspect,lambda x: quit(),False),
]

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                button.update(event.pos,buttons)

    for button in buttons:
        button.render(SCREEN)
    pygame.display.flip()
    SCREEN.fill(bgColor)
pygame.quit()