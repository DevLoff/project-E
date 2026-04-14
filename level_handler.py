import json
import pygame
from objects.level_obj import Level
# Make sure these imports match your actual file names/locations
from objects.visual_obj import Cloud, Port, Field, Peg
from objects.physic_obj import *

import time

# At the top of the file
LAST_LOAD_TIME = 0


def load_level(path, root):
    global LAST_LOAD_TIME
    current_time = time.time()

    # If we tried to load a level less than 0.5 seconds ago, REJECT IT
    if current_time - LAST_LOAD_TIME < 0.5:
        return None

    LAST_LOAD_TIME = current_time
    print(f"--- VALID LOAD STARTING: {path} ---")

    try:
        # CHANGE: Use 'path' here, NOT 'filename'
        with open(path, 'r') as f:
            data = json.load(f)
            print("LOADING FILE:", path)
            print("DEBUG JSON next_level_file:", data.get("next_level_file"))
            print("DATA:", data)
    except FileNotFoundError:
        print(f"CRITICAL ERROR: Could not find the file: {path}")
        return None

    print("LEVEL LOADED WITH NEXT:", data.get("next_level_file"))

    # CHANGE: Use 'root' (the argument), NOT 'root_menu'
    lvl = Level(ori=root)

    # 1. Background Setup
    try:
        if isinstance(data["bg"], str):
            bg_img = pygame.image.load(data["bg"]).convert()
        else:
            bg_img = pygame.Surface((800, 600))
            bg_img.fill((20, 20, 60))
    except Exception as e:
        print(f"Warning: Could not load background {data['bg']}: {e}")
        bg_img = pygame.Surface((800, 600))
        bg_img.fill((100, 0, 0))

        # 2. Ports (Launchers)
    for p in data["ports"]:
        lvl.add_port(Port(pygame.Vector2(p["pos"]), pygame.image.load(p["img"])))

    # 3. Pegs (Seeds)
    for p_data in data["pegs"]:
        img = pygame.image.load(p_data["img"])
        lvl.add_peg(Peg(p_data["rad"], img))

    # 4. Bench Positioning
    lvl.arrange_bench(data["bench"], data["space"])

    # 5. Clouds & Hitboxes
    for c in data["clouds"]:
        cloud_pos = pygame.Vector2(c["pos"])
        cloud_img = pygame.image.load(c["img"])
        hitboxes = []

        for h in c["hitboxes"]:
            if h["type"] == "circle":
                abs_pos = cloud_pos + pygame.Vector2(h["opts"]["pos"])
                hitboxes.append(Circle(abs_pos, h["opts"]["rad"]))
            elif h["type"] == "line":
                p1 = cloud_pos + pygame.Vector2(h["opts"]["one"])
                p2 = cloud_pos + pygame.Vector2(h["opts"]["two"])
                hitboxes.append(Line(p1, p2))

        # --- FIX: Move Cloud creation OUTSIDE the hitbox loop ---
        new_cloud = Cloud(cloud_pos, cloud_img)
        new_cloud.hitboxes = hitboxes
        lvl.add_cloud(new_cloud)

    # 6. Fields (Targets)
    for f in data["fields"]:
        lvl.add_field(Field(pygame.Vector2(f["pos"]), pygame.image.load(f["img"])))

    # 7. Progression & Initialization
    lvl.next_level_json = data.get("next_level_file")
    print(f"DEBUG: Loader found next level as: {lvl.next_level_json}")
    lvl.set_staticlayers(bg_img)
    return lvl