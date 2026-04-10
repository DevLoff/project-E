import pygame

def handle_imglike(data) -> pygame.Surface:
    if type(data) == pygame.Surface:
        return data
    if type(data) == str:
        return pygame.image.load(data)
    return pygame.Surface((0,0))