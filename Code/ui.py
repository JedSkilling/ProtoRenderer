from settings import *
from pygameInit import *
from functions import *

print("Loading UI module")

def setup_ui():
    screen.fill(background_color)
    centre = SCtoActualCoord((0, 0))
    pygame.draw.rect(screen, centreCol, [centre[0]-1,centre[1]-5,2,10])
    pygame.draw.rect(screen, centreCol, [centre[0]-5,centre[1]-1,10,2])


