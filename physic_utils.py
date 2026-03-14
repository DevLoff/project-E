import pygame
import math

def deg_to_rad(t):
    return t*math.pi/180
def natural_angle(vec):
    return deg_to_rad(pygame.Vector2(1,0).angle_to(vec))