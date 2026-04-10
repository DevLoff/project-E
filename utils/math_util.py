import pygame
import math

from objects.math_obj import Matrix2

def deg_to_rad(t):
    return t*math.pi/180
def rad_to_deg(t):
    return t*180/math.pi
def natural_angle(vec):
    return deg_to_rad(pygame.Vector2(1,0).angle_to(vec))
def radial_vec(r,a):
    return r * pygame.Vector2(math.cos(a),math.sin(a))
def create_identity_matrix(q=1):
    return Matrix2(q,0,0,q)