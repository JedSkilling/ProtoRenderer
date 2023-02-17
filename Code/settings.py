import numpy as np
from functions import quatFromRotAndAxis

print("Loading settings")

#   Aesthetics

background_color = np.array((20,10,30))
lineColour = np.array((255, 255, 255))
lineThickness = 4
centreCol = np.array((200, 200, 200))


#   Video settings

perspective_projection = True
wireframe = False
fps = 30
FoV = 90    #  FoV in DEGREES
scale = 1000
mouseSensitivity = 400

minDistanceFromCamera = 0
camBackwardsOffset = 0


#   Positional arguments
init_camera_rotation = np.array((0,0,0), float)
init_camera_pos = np.array((0, 0, 0), float)
cameraDefaultRotation = quatFromRotAndAxis(0, np.array((1, 0, 0)))

maxAcceleration = 0.01
maxVelocity = 0.2



#   Constants
