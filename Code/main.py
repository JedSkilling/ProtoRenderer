from ctypes import WinDLL
import math
import pygame
import numpy as np
import copy
import time

#   Import everything else
from pygameInit import *
from classes import * 
from settings import *
from ui import *
from renderingShortcuts import *

def getAllLines(camera):    #   Gets all the lines that will need to be drawn for a specific camera
    currDrawList = []
    for singleTriangle in allTriangles: #   Loops through every camera in the 3D world
        if(lighting):
            newDrawList = singleTriangle.getDrawList(camera, wireframe, light1)
        else:
            newDrawList = singleTriangle.getDrawList(camera, wireframe)
        if(not type(newDrawList) == type(None)):
            #print(type(newDrawList))
            if(wireframe):
                for i in range(0, len(newDrawList)):
                    currDrawList.append(newDrawList[i])
            else:
                currDrawList.append(newDrawList)
    
    if(not type(currDrawList) == type(None)):
        surf = surface_DrawLines
        for i in range(0, len(currDrawList)):
            if(wireframe):

                point1 = currDrawList[i][0]
                point2 = currDrawList[i][1]
                mainLineList.append([surf, point1.color, point1.drawPos, point2.drawPos, lineThickness])
            else:
                
                #   Take mean colour
                color = currDrawList[i][1]*mean3(currDrawList[i][0][0].color, currDrawList[i][0][1].color, currDrawList[i][0][2].color)
                color = np.clip(color, 0, 255)
                triangle = [currDrawList[i][0][0].drawPos, currDrawList[i][0][1].drawPos, currDrawList[i][0][2].drawPos]
                
                dist = magnitude(mean3(currDrawList[i][0][0].pos, currDrawList[i][0][1].pos, currDrawList[i][0][2].pos) - camera.pos)
                #print(dist)
                #mainPolygonListDetail.append([centerOfTriangle])


                mainPolygonList.append([surf, color, triangle, 0, dist])
        if(not wireframe):
            mainPolygonList.sort(key=getSortVal, reverse=True)

    
        
            
# Define the triangle vertices
# triangle = [(400, 100), (500, 500), (300, 500)]

# Fill the triangle with a solid color
# pygame.draw.polygon(screen, (255, 0, 0), triangle, 0)
        
def drawAllLines():
    if(wireframe):
        for line in mainLineList:
            pygame.draw.line(*line)
    else:
        for triangle in mainPolygonList:
            pygame.draw.polygon(*triangle[:4])


def handleKeyPresses():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        cam1.acc += np.array((0, 0, 1))
    if keys[pygame.K_s]:
        cam1.acc += np.array((0, 0, -1))
    if keys[pygame.K_d]:
        cam1.acc += np.array((0, 1, 0))
    if keys[pygame.K_a]:
        cam1.acc += np.array((0, -1, 0))            
    if keys[pygame.K_SPACE]:
        cam1.acc += np.array((-1, 0, 0))
    if keys[pygame.K_LCTRL]:
        cam1.acc += np.array((1, 0, 0))



#   Defining objects

allTriangles = []
'''
v1 = (100, 50, -51)
v2 = (100, -51, 52)
v3 = (100, 52, 53)
T1VInfo = np.array((v1, v2, v3))
T1 = Triangle((0, 0, 0), (0, 1, 0, 0), T1VInfo)
allTriangles.append(T1)

v4 = (160, 100, -50)
v5 = (160, 150, -50)
v6 = (160, 100, -100)
T2VInfo = np.array((v4, v5, v6))
T2 = Triangle((0, 200, 0), (0, 1, 0, 0), T2VInfo)
allTriangles.append(T2)
'''
    #   Blender uses COUNTER CLOCKWISE winding

cubeLocation1 = (0, 0, 10)  #   x,y,z
allTriangles += makeCuboid(cubeLocation1, (8, 2, 2), quatFromRotAndAxis(math.pi, np.array((0, 1, 0))), sideRemoval=[3])

cubeLocation2 = (0, 10, 10)
allTriangles += makeCuboid(cubeLocation2, (8, 2, 2), quatFromRotAndAxis(math.pi, np.array((0, 1, 0))), sideRemoval=[3])

cubeLoc3 = (-10, -2, 8)
allTriangles += makeCuboid(cubeLoc3, (2, 16, 2), quatFromRotAndAxis(0, np.array((1, 0, 0))))



cubeLoc4 = (-0.1,3,3)
allTriangles += makeCuboid(cubeLoc4, (0.1, 2, 2), quatFromRotAndAxis(math.pi/10, np.array((1, 0.001, 0))))

cubeLoc5 = (-0.1,6,1)
allTriangles += makeCuboid(cubeLoc5, (0.1, 2, 2), quatFromRotAndAxis(-math.pi/10, np.array((1, 0, 0.01))))


#cubeDebug01 = (-1,-1,4)
#allTriangles += makeCuboid(cubeDebug01, (2, 2, 2), quatFromRotAndAxis(0, np.array((1, 0, 0))))
'''
tmpVertices = np.zeros((3, 3))

tmpVertices[0] = (2, 0, 1)        #   A 
tmpVertices[1] = (2, 4, 0)       #   B

tmpVertices[2] = (2, 0, 4)       #   D
triangleLocation = np.array((0, 0, 0))
rotation = quatFromRotAndAxis(0, np.array((1, 0, 0)))
T1 = Triangle(triangleLocation, rotation, np.array((tmpVertices[0], tmpVertices[1], tmpVertices[2])))
allTriangles.append(T1)
'''
if(lighting):
    light1pos = np.array((-15, -4, -4))
    light1vel = np.array((0, 0, 0))
    light1acc = np.array((0, 0, 0))
    motionInfo = np.array((light1pos, light1vel, light1acc))

    light1 = lightSource(motionInfo, 150)


cam1 = Camera(copy.deepcopy(init_camera_pos), init_camera_rotation, FoV)




mainLineList = []

mousePrev = np.array(pygame.mouse.get_pos(), float)
centerScreen = np.array((width/2, height/2))

t = 0


deltaFoV = 0
focussed = True
if(focussed):
    
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.mouse.get_rel()
    

running = True
clock = pygame.time.Clock()
#   Main Gameplay loop
while running:

    setup_ui()  
    surface_DrawLines.fill((background_color))
    cam1.acc = np.zeros(3)

    if(focussed):
        deltaMousePos = np.array(pygame.mouse.get_rel(), float)
    else:
        deltaMousePos = np.zeros(2)
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                cam1.resetPlayerChanges()
            if event.key == pygame.K_f:
                focussed = not focussed
                pygame.mouse.set_visible(not focussed)
                pygame.event.set_grab(focussed)
                pygame.mouse.get_rel()
            if event.key == pygame.K_t:
                deltaFoV += 5
            if event.key == pygame.K_g:
                deltaFoV -= 5
            if event.key == pygame.K_v:
                cam1.vel = np.zeros(3)
            if event.key == pygame.K_p:
                wireframe = not wireframe




    cam1.updateSettings(FoV + deltaFoV) #   TEMP - Not that great
    
    
    fullNewRotation = np.zeros(3)
    fullNewRotation[0] = -deltaMousePos[0]
    fullNewRotation[1] = deltaMousePos[1]
    fullNewRotation[2] = 0
    
    

    #print(f"Full new Rotation: {fullNewRotation}")
    cam1.updateRotationInformation(fullNewRotation/mouseSensitivity)
    
     

    #   Normalise acceleration for cameras from keys to avoid strafing being better
    handleKeyPresses()
    cam1.acc = normalise(cam1.acc, maxAcceleration)

    mainPolygonListDetail = []
    mainPolygonList = []
    mainLineList = []

    cam1.updateMotion()
    if(lighting):
        light1.updatePos()


    

    smallfont = pygame.font.SysFont('Corbel',15)
    
    mouseInfo = f"Mouse Movement: {deltaMousePos}"
    cam1Pos = f"Pos: {cam1.pos}"
    cam1Vel = f"Vel: {cam1.vel}"
    cam1Acc = f"Acc: {cam1.acc}"
    timeInfo = f"t:{t}"
    cam1VelMagnitude = f"Speed:{magnitude(cam1.vel)}"
    

    mouseText = smallfont.render(mouseInfo, True , (255,255,255))
    camPosText = smallfont.render(cam1Pos, True, (255, 255, 255))
    camVelText = smallfont.render(cam1Vel, True, (255, 255, 255))
    camAccText = smallfont.render(cam1Acc, True, (255, 255, 255))
    camVelMagnitudeText = smallfont.render(cam1VelMagnitude, True, (255, 255, 255))
    timeText = smallfont.render(timeInfo, True , (255,255,255))
    

    


    getAllLines(cam1)
    drawAllLines()

    #   Game blits
    screen.blit(surface_DrawLines,(0,0))

    pygame.draw.rect(screen,(140,140,150),[0,0,180,120])
    screen.blit(mouseText, (10,10))

    #   Info blits
    screen.blit(camPosText, (10, 25))
    screen.blit(camVelText, (10, 40))
    screen.blit(camAccText, (10, 55))
    screen.blit(camVelMagnitudeText, (10, 70))

    screen.blit(timeText, (10, 85))

    pygame.display.update()
    clock.tick(fps)
    t=t+1
    