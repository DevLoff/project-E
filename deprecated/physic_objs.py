from deprecated.physic_utils import *

class StaticObj:
    def __init__(self,rough=1.0):
        self.roughness = rough
    def get_setters(self) -> list:
        pass
    def proximity(self, point) -> float:
        pass
    def detection_area(self, point) -> bool:
        pass
    def render(self, surface, color) -> pygame.Rect:
        pass

"""
class ArcStatic(StaticObj):
    def __init__(self,rectangle,start_deg,end_deg) -> None:
        self.area = pygame.Rect(rectangle)
        self.color = pygame.Color(255,255,255)
        self.startAngle = start_deg
        self.endAngle = end_deg
        self.vecCenter = pygame.Vector2(self.area.center)
        self.halfsize = pygame.Vector2(self.area.size)/2
        self.startPoint = pygame.Vector2(round(self.halfsize.x*math.cos(start_deg),5),  round(self.halfsize.y*math.sin(start_deg),5)) + self.vecCenter
        self.endPoint = pygame.Vector2(round(self.halfsize.x*math.cos(end_deg),5),  round(self.halfsize.y*math.sin(end_deg),5)) + self.vecCenter
        self.radius = lambda alpha : round(math.sqrt((self.halfsize.x*math.cos(alpha))**2 + (self.halfsize.y*math.sin(alpha))**2),5)
        self.acute = abs(end_deg - start_deg) < math.pi
        self.startBracket = self.norm(self.startPoint).rotate(-90)
        self.endBracket = self.norm(self.endPoint).rotate(90)

    def norm(self,point) -> pygame.Vector2:
        trace = (self.vecCenter - point)
        if trace != pygame.Vector2():
            return trace.normalize()
        return trace

    def update(self,rectangle,start_deg,end_deg):
        self.area = pygame.Rect(rectangle)
        self.startAngle = start_deg
        self.endAngle = end_deg
        self.vecCenter = pygame.Vector2(self.area.center)
        self.halfsize = pygame.Vector2(self.area.size) / 2
        self.startPoint = pygame.Vector2(round(self.halfsize.x * math.cos(start_deg), 5),
                                         round(self.halfsize.y * math.sin(start_deg), 5)) + self.vecCenter
        self.endPoint = pygame.Vector2(round(self.halfsize.x * math.cos(end_deg), 5),
                                       round(self.halfsize.y * math.sin(end_deg), 5)) + self.vecCenter
        self.radius = lambda alpha: round(
            math.sqrt((self.halfsize.x * math.cos(alpha)) ** 2 + (self.halfsize.y * math.sin(alpha)) ** 2), 5)
        self.norm = lambda point: (self.vecCenter - point).normalize()
        self.acute = abs(end_deg-start_deg)<math.pi
        self.startBracket = self.norm(self.startPoint).rotate(-90)
        self.endBracket = self.norm(self.endPoint).rotate(90)

    def proximity(self, point) -> float:
        studiedPoint = pygame.Vector2(point)-self.vecCenter
        return self.radius(natural_angle(studiedPoint))-studiedPoint.length()

    def detection_area(self, point) -> bool:
        studiedPoint = pygame.Vector2(point)
        return ((self.startBracket.dot(studiedPoint-self.startPoint)>0) + (self.endBracket.dot(studiedPoint-self.endPoint)>0)) >= 1 + self.acute

    def normal(self,vec,point=(0,0)) -> pygame.Vector2:
        studiedPoint = pygame.Vector2(point)
        return -vec.project(self.norm(studiedPoint))

    def render(self,surface) -> pygame.Rect:
        return pygame.draw.arc(surface,self.color,self.area,-self.endAngle,-self.startAngle)

    def render_debug(self, surface) -> pygame.Rect:
        return pygame.draw.line(surface, (255, 255, 255), self.startPoint, self.endPoint)

class LineStatic(StaticObj):
    def __init__(self,start_point,end_point) -> None:
        self.color = pygame.Color(255,255,255)
        self.startPoint = pygame.Vector2(start_point)
        self.endPoint = pygame.Vector2(end_point)
        lowcorner = pygame.Vector2(min(self.startPoint.x,self.endPoint.x),min(self.startPoint.y,self.endPoint.y))
        highcorner = pygame.Vector2(max(self.startPoint.x, self.endPoint.x), max(self.startPoint.y, self.endPoint.y))
        super().__init__(lowcorner,highcorner-lowcorner)
        self.startBracket = (self.endPoint-self.startPoint).normalize()
        self.endBracket = (self.startPoint - self.endPoint).normalize()
        self.norm = self.startBracket.rotate_rad(math.pi/2)

    def update(self,start_point,end_point):
        self.startPoint = pygame.Vector2(start_point)
        self.endPoint = pygame.Vector2(end_point)
        self.startBracket = (self.endPoint - self.startPoint).normalize()
        self.endBracket = (self.startPoint - self.endPoint).normalize()
        self.norm = self.startBracket.rotate_rad(math.pi / 2)

    def proximity(self,point) -> float:
        studiedPoint = pygame.Vector2(point)-self.startPoint
        return self.norm.dot(studiedPoint)

    def detection_area(self, point) -> bool:
        studiedPoint = pygame.Vector2(point)
        return self.startBracket.dot(studiedPoint - self.startPoint) > 0 and self.endBracket.dot(studiedPoint - self.endPoint) > 0

    def normal(self,vec,point=None) -> pygame.Vector2:
        return -vec.project(self.norm)

    def render(self,surface) -> pygame.Rect:
        return pygame.draw.line(surface,self.color,self.startPoint,self.endPoint)
"""

class DiscBody:
    def __init__(self,radius,initial_pos=(0,0),initial_vel=(0,0),bounce=0.0) -> None:
        self.radius = radius
        self.pos = pygame.Vector2(initial_pos)
        self.velocity = pygame.Vector2(initial_vel)
        self.bounciness = bounce

    def copy(self):
        return DiscBody(self.radius,self.pos.copy(),self.velocity.copy(),self.bounciness)

    def render(self,surface) -> pygame.Rect:
        return pygame.draw.circle(surface, (255,255,255), self.pos, self.radius)

    def static_collision_phy(self,dt,grav,res,traces):
        collided,difference,overshot,friction,rep = False,0,0,1,pygame.Vector2()
        self.velocity = (self.velocity + grav * dt) * res
        after = self.pos.copy() + self.velocity.copy() * dt
        for trace in traces:
            difference,overshot = trace.proximity(self.pos),trace.proximity(after)
            if difference * overshot < 0.0:
                overshot = difference - overshot
            if abs(overshot) < self.radius and trace.detection_area(after):
                normalForce = trace.normal(after) * (self.radius/overshot)
                self.velocity = self.velocity.project(normalForce.rotate(90)) - self.bounciness * self.velocity.project(normalForce)
                self.pos += normalForce
                friction *= trace.roughness
                collided = True
                rep += normalForce
        self.velocity *= friction
        self.pos += self.velocity * dt
        return collided,difference,overshot,rep

# WIP SECTION

class ProtoArc(StaticObj):
    def __init__(self,center,fpoint,spoint) -> None:
        super().__init__()
        self.update(center,fpoint,spoint)

    def update(self,center,fpoint,spoint) -> None:
        self.vecCenter = pygame.Vector2(center)
        self.startPoint = pygame.Vector2(fpoint)
        self.endPoint = pygame.Vector2(spoint)
        self.startRel,self.endRel = (self.startPoint-self.vecCenter,self.endPoint-self.vecCenter)
        self.elipticMat = Matrix2(self.startRel,self.endRel)
        self.startAngle = natural_angle(self.startRel)
        self.endAngle = natural_angle(self.endRel)
        self.span = abs(self.endAngle - self.startAngle)
        self.acute = self.span < math.pi
        self.startBracket = self.normal(self.startPoint).rotate(90)
        self.endBracket = self.normal(self.endPoint).rotate(-90)

    def eliptic_angle(self,alpha):
        return natural_angle(self.elipticMat.inverse() * radial_vec(1,alpha))

    def radius(self,alpha):
        return (self.elipticMat * radial_vec(1,self.eliptic_angle(alpha))).length()

    def normal(self,point) -> pygame.Vector2:
        """
        studiedAngle = natural_angle(pygame.Vector2(point)-self.vecCenter)
        studiedRef = self.elipticMat.inverse() * pygame.Vector2(math.cos(studiedAngle),-math.sin(studiedAngle))
        """
        studiedRef = pygame.Vector2(point) - self.vecCenter
        if studiedRef.length() == 0:
            return studiedRef.copy()
        return studiedRef.normalize()

    def proximity(self, point) -> float:
        studiedPoint = pygame.Vector2(point)-self.vecCenter
        return studiedPoint.length()-self.radius(natural_angle(studiedPoint))

    def detection_area(self, point) -> bool:
        studiedPoint = pygame.Vector2(point)
        return ((self.startBracket.dot(studiedPoint-self.startPoint)>0) + (self.endBracket.dot(studiedPoint-self.endPoint)>0)) >= 1 + self.acute

    def render(self,surface,color) -> pygame.Rect:
        rank = (math.pi/180)
        return pygame.draw.lines(surface,color,False,
            [self.elipticMat * radial_vec(1,k*rank) + self.vecCenter for k in range(90)])

    def debug_render(self,surface):
        rects = [
            pygame.draw.circle(surface,(255,0,0),self.vecCenter,3),
            pygame.draw.line(surface, (255, 0, 0), self.startPoint, self.vecCenter),
            pygame.draw.line(surface, (255, 0, 0), self.endPoint, self.vecCenter),
            pygame.draw.lines(surface, (255,255,255), False,
                              [self.elipticMat * radial_vec(1, k * (math.pi/180)) + self.vecCenter for k in range(360)])
        ]
        return rects

class ProtoLine(StaticObj):
    def __init__(self,start_point,end_point) -> None:
        super().__init__()
        self.startPoint = pygame.Vector2(start_point)
        self.endPoint = pygame.Vector2(end_point)
        self.update_relatives()

    def set_startpoint_ip(self,disp):
        self.startPoint += pygame.Vector2(disp)
        self.update_relatives()
    def set_endpoint_ip(self,disp):
        self.endPoint += pygame.Vector2(disp)
        self.update_relatives()

    def get_setters(self):
        return [
            self.set_startpoint_ip,
            self.set_endpoint_ip,
        ]

    def update_relatives(self) -> None:
        self.startBracket = (self.endPoint - self.startPoint).normalize()
        self.endBracket = (self.startPoint - self.endPoint).normalize()
        self.norm = self.startBracket.rotate(90)

    def proximity(self,point) -> float:
        studiedPoint = pygame.Vector2(point)-self.startPoint
        return self.norm.dot(studiedPoint)

    def detection_area(self, point) -> bool:
        studiedPoint = pygame.Vector2(point)
        return self.startBracket.dot(studiedPoint - self.startPoint) > 0 and self.endBracket.dot(studiedPoint - self.endPoint) > 0

    def normal(self,point) -> pygame.Vector2:
        return self.norm

    def render(self,surface,color=(255,255,255)):
        marks = []
        if color == (255,255,0):
            marks = self.debug_render(surface)
        return marks + [pygame.draw.line(surface,color,self.startPoint,self.endPoint)]

    def debug_render(self,surface):
        return [
            pygame.draw.circle(surface, (255, 0, 0), self.startPoint, 5),
            pygame.draw.circle(surface, (255, 0, 0), self.endPoint, 5),
        ]

class BetterArc(StaticObj):
    def __init__(self,center,mvertex,mradius,sangle,eangle) -> None:
        super().__init__()
        self.center = pygame.Vector2(center)
        self.mVertex = pygame.Vector2(mvertex)
        self.minRadius = mradius
        self.startAngle = min(sangle,eangle)
        self.endAngle = max(sangle,eangle)
        self.update_relatives()

    def set_center_ip(self,disp) -> None:
        self.center += pygame.Vector2(disp)
        self.mVertex += pygame.Vector2(disp)
        self.update_relatives()
    def set_mvertex_ip(self,disp) -> None:
        self.mVertex += pygame.Vector2(disp)
        self.update_relatives()
    def set_mradius_ip(self,disp) -> None:
        self.minRadius += pygame.Vector2(disp).dot(self.minVertexRel.normalize())
        self.update_relatives()
    def set_sangle_ip(self,disp) -> None:
        self.startAngle = natural_angle(pygame.Vector2(disp) + self.startPoint - self.center)
        self.update_relatives()
    def set_eangle_ip(self,disp) -> None:
        self.endAngle = natural_angle(pygame.Vector2(disp) + self.endPoint - self.center)
        self.update_relatives()

    def get_setters(self) -> list:
        return [
            self.set_center_ip,
            self.set_mvertex_ip,
            self.set_mradius_ip,
            self.set_sangle_ip,
            self.set_eangle_ip
        ]

    def update_relatives(self):
        if (self.mVertex - self.center).length() > self.minRadius:
            self.majVertexRel = self.mVertex - self.center
            self.minVertexRel = self.majVertexRel.normalize().rotate(90) * self.minRadius
        else:
            self.minVertexRel = self.mVertex - self.center
            self.majVertexRel = self.minVertexRel.normalize().rotate(90) * self.minRadius
        self.focusRel = self.majVertexRel.normalize() * math.sqrt(max(self.majVertexRel.length() ** 2 - self.minVertexRel.length() ** 2,0))
        self.fFocusPoint, self.sFocusPoint = self.center + self.focusRel, self.center - self.focusRel
        self.ellipticPlane = Matrix2(self.majVertexRel, self.minVertexRel)
        self.startPoint = radial_vec(self.radius(self.startAngle), self.startAngle) + self.center
        self.endPoint = radial_vec(self.radius(self.endAngle), self.endAngle) + self.center
        self.startBracket = (self.startPoint-self.center).rotate(90)
        self.endBracket = (self.endPoint-self.center).rotate(-90)

    def elliptic_angle(self,alpha):
        return natural_angle(self.ellipticPlane.inverse() * radial_vec(1,alpha))
    def radius(self,alpha) -> float:
        return (self.ellipticPlane * radial_vec(1,self.elliptic_angle(alpha))).length()

    def normal(self,point) -> pygame.Vector2:
        studiedAngle = natural_angle(pygame.Vector2(point) - self.center)
        studiedPoint = radial_vec(self.radius(studiedAngle), studiedAngle)
        fpath,spath = - self.focusRel - studiedPoint, self.focusRel - studiedPoint
        complAngle = (natural_angle(fpath) + natural_angle(spath)) / 2
        return radial_vec(-1, complAngle)

    def proximity(self, point) -> float:
        studiedPoint = pygame.Vector2(point)-self.center
        return studiedPoint.length()-self.radius(natural_angle(studiedPoint))

    def detection_area(self, point) -> bool:
        studiedPoint = pygame.Vector2(point)
        return ((self.startBracket.dot(studiedPoint-self.startPoint)>0) + (self.endBracket.dot(studiedPoint-self.endPoint)>0)) == 2

    def render(self,surface,color=(255,255,255)):
        marks = []
        if color == (255,255,0):
            marks = self.debug_render(surface)
        sAngle,eAngle = rad_to_deg(self.startAngle)%360,rad_to_deg(self.endAngle)%360
        rank,points = math.pi/180,[]
        for k in range(int(abs(eAngle-sAngle))+1):
            alpha = k*rank + self.startAngle
            points.append(radial_vec(self.radius(alpha),alpha) + self.center)
        if len(points)>1:
            return marks + [pygame.draw.lines(surface,color,False,points)]
        return marks

    def debug_render(self,surface):
        rects = [
            pygame.draw.circle(surface,(255,0,0),self.center,3),
            pygame.draw.circle(surface, (255, 0, 255), self.mVertex, 3),
            pygame.draw.circle(surface, (255, 0, 0), self.startPoint, 5),
            pygame.draw.circle(surface, (255, 0, 0), self.endPoint, 5),
            pygame.draw.line(surface, (255, 0, 255), self.majVertexRel * 1.1 + self.center, self.center),
            pygame.draw.line(surface, (255, 0, 255), self.minVertexRel * 1.1 + self.center, self.center),
            pygame.draw.line(surface, (255, 0, 0), (self.startPoint-self.center)*1.1 + self.center, self.center),
            pygame.draw.line(surface, (255, 0, 0), (self.endPoint-self.center)*1.1 + self.center, self.center),
            pygame.draw.lines(surface, (255,255,255), False,
                              [radial_vec(self.radius(k*(math.pi/180)),k*(math.pi/180)) + self.center for k in range(360)])
        ]
        return rects