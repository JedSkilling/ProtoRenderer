import pygame

print("Initialising pygame")

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width = screen.get_width()
height = screen.get_height()

surface_DrawLines = pygame.Surface((width,height))


pygame.display.set_caption("3D Rendering")

mainDrawList = list