from objects.level_obj import Level
from objects.visual_obj import Port, Peg, Cloud, Field
from objects.physic_obj import Circle, Line
from utils.image_util import handle_imglike


def assertions(param,*tags):
    for tag in tags:
        assert (tag in param)

def transform_raw(param):
    assert ("type" in param)
    if param["type"] == "level":
        return charge_level(param)
    return charge_menu(param)

def charge_level(param):
    assertions(param, "ports", "pegs", "clouds", "fields", "bench", "space", "bg")
    level = Level()
    for port in param["ports"]:
        level.add_port(charge_port(port))
    for peg in param["pegs"]:
        level.add_peg(charge_peg(peg))
    for cloud in param["clouds"]:
        level.add_cloud(charge_cloud(cloud))
    for field in param["fields"]:
        level.add_field(charge_field(field))
    level.rack_peg()
    level.arrange_bench(param["bench"],param["space"])
    level.set_staticlayers(
        handle_imglike(param["bg"])
    )
    return level

def charge_port(param):
    assertions(param,"pos","img")
    return Port(param["pos"],param["img"])

def charge_peg(param):
    assertions(param,"rad","img")
    return Peg(param["rad"],param["img"])

def charge_cloud(param):
    assertions(param,"pos","img","hitboxes")
    cloud = Cloud(param["pos"],param["img"])
    for hitbox in param["hitboxes"]:
        cloud.add_hitbox(charge_hitbox(hitbox))
    return cloud

def charge_hitbox(param):
    assertions(param,"type","opts")
    if param["type"] == "circle":
        return charge_circle(param["opts"])
    return charge_line(param["opts"])

def charge_circle(param):
    assertions(param,"pos","rad")
    return Circle(param["pos"],param["rad"])

def charge_line(param):
    assertions(param,"one","two")
    return Line(param["one"],param["two"])

def charge_field(param):
    assertions(param,"pos","img")
    return Field(param["pos"],param["img"])

def charge_menu(param): # TODO
    pass