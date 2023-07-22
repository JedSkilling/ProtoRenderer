import math
import pygame
import numpy as np
import time
import cmath
from pyquaternion import Quaternion as quaternion
import copy
import random

from settings import *
from pygameInit import *
from functions import *


print("Importing Classes")

class Triangle:
    def __init__(self, pos, rotation, verticeInfo) -> None:
        self.pos = pos
        self.rotation = rotation
        self.vertices = np.zeros(3, Vertex) #   The array of vertexes that make up each triangle
        self.drawList = np.zeros((3, 2))

        for i in range(0, 3):
            self.vertices[i] = Vertex(verticeInfo[i], i)

        self.normal = normalise(cross(self.vertices[1].relPos - self.vertices[0].relPos, self.vertices[2].relPos - self.vertices[1].relPos))
        self.center = self.pos + mean3(self.vertices[0].relPos, self.vertices[1].relPos, self.vertices[2].relPos)

    def rotate(self, newRotation):
        self.rotation = newRotation * self.rotation * newRotation.conjugate

    def getRot(self):
        return self.rotation
    
    def getPos(self):
        return self.pos
    
    def getDrawList(self, Camera, isWireframe, light=None):
        self.drawList = np.zeros((3, 2), Vertex)
        outOfShot = 0
        isFacingCamera = True
        #self.center = mean3(self.vertices[0].relPos, self.vertices[1].relPos, self.vertices[2].relPos)
        if(not isWireframe):
            #camDirection = rotateByQuaternion(Camera.rotQuat, np.array((0, 0, 1)))
            #print(f"Center; {self.center} Camera: {Camera.pos}")
            vectorFromCenterToCam = normalise(self.center - Camera.pos)
            #print(f"Normal: {self.normal} Vec from cam to Center: {vectorFromCenterToCam}\nDot product is: {dot(self.normal, vectorFromCenterToCam)}")
            if(dot(self.normal, vectorFromCenterToCam) <= 0):
                isFacingCamera = False

            if(lighting):
                vectorFromCenterToLight = normalise(self.center - light.pos)
                #print(f"Normal: {self.normal} Vec from cam to Center: {vectorFromCenterToCam}\nDot product is: {dot(self.normal, vectorFromCenterToCam)}")
                lightingMag = dot(self.normal, vectorFromCenterToLight)
                if(lightingMag > 0):
                    self.lighting = (light.brightness/100) * lightingMag
                else:
                    self.lighting = 0.119
            else:
                self.lighting = 1
            
            
        #print(f"self vertices: {self.vertices}")
        for point in self.vertices:
            #print(f"Curr point: {point}")
            point.updatePosAndRot(self)
            distanceFromCam = point.getScreenPos(Camera)
            if(point.outOfShot):
                outOfShot += 1
            if(distanceFromCam < minDistanceFromCamera):
                outOfShot = 3
            
        
        if(outOfShot >= 3):
            #print("All out of shot")
            return None
        
        if(isWireframe):
            self.drawList[0][0] = self.vertices[0]
            self.drawList[0][1] = self.vertices[1]

            self.drawList[1][0] = self.vertices[1]
            self.drawList[1][1] = self.vertices[2]

            self.drawList[2][0] = self.vertices[2]
            self.drawList[2][1] = self.vertices[0]
        else:
            
            self.drawList = [self.vertices, self.lighting]
            

        

        if(isFacingCamera):
            return self.drawList
        else:
            return
                

class Vertex:
     #  Each Vertex is a vector from a set corner of the Triangle
     #  Future cases should add colour, weighting ect
    def __init__(self, relPos, colID) -> None:
        self.rotation = None
        self.relPos = relPos
        if(colID == 0):
            self.color = np.array((255, 0, 0))
        elif(colID == 1):
            self.color = np.array((0, 255, 0))
        elif(colID == 2):
            self.color = np.array((0, 0, 255))
        else:
            self.color = np.array((255, 255, 255))
        self.color = np.array((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))  #   Set all color to the same
        self.pos = None
        self.SCpos = 0
        
        self.outOfShot = False
        

    def getScreenPos(self, camera):
        tmpPos = self.pos
        
        wrkPos = tmpPos - camera.pos

        wrkPos = rotateByQuaternion(camera.rotQuat.conjugate, wrkPos)
        #print(f"WrkPos before: {wrkPos}")
        #print(f"Roation by: {camera.rotQuat.conjugate}")
        
        #print(f"WrkPos after: {wrkPos}")
        '''
        wrkPosMagnitude = sum(wrkPos*wrkPos)
        wrkPosNormalised = wrkPos/wrkPosMagnitude
        
        wrkPosQuaternion = camera.rotQuat.conj()*np.quaternion(0, wrkPosNormalised[0], wrkPosNormalised[1], wrkPosNormalised[2])*camera.rotQuat
        wrkPos = wrkPosMagnitude*np.array((wrkPosQuaternion.x, wrkPosQuaternion.y, wrkPosQuaternion.z))
        '''
        
        
        if(not wrkPos[2] == 0):
            #   If behind, z will be negative
            #print(f"Camera FoV: {camera.FoV}")
            #print(f"Tan of angle{math.tan(camera.FoV)}")
            if(perspective_projection):
                #print("Getting Screen coords, showing pre then after")
                #print(wrkPos[2])

                wrkPos[0] = (wrkPos[0]*math.tan(camera.FoV))/(wrkPos[2]+camBackwardsOffset)  #   By offsetting the cameras position I avoided most of the scaling issues?
                wrkPos[1] = (wrkPos[1]*math.tan(camera.FoV))/(wrkPos[2]+camBackwardsOffset)

            distanceFromCamera = wrkPos[2]
            wrkPos[2] /= abs(wrkPos[2])
            self.SCpos = wrkPos
            #print(f"Screen Pos after:{self.SCpos}")
            self.isInScreenBound(camera)
            
            #print(f"Draw Pos after:{self.drawPos}")
        else:
            self.outOfShot = True
            distanceFromCamera = 0
            self.SCpos = wrkPos
        
        self.drawPos = SCtoActualCoord(self.SCpos[:2])


        return distanceFromCamera
        
        

    def isInScreenBound(self, camera):
        tmpScreenCoord = SCtoActualCoord(self.SCpos[:2])
        if(camera.bounds[0] > tmpScreenCoord[0] or camera.bounds[1] < tmpScreenCoord[0] or camera.bounds[2] > tmpScreenCoord[1] or camera.bounds[3] < tmpScreenCoord[1] or self.SCpos[2] < 1):
            #print(f"Point found to not be in screen bounds\nPoint real coord is {self.pos}\nPoint screen coord is {SCtoActualCoord(self.SCpos[:2])}")
            
            '''
            if(camera.bounds[0] > self.SCpos[0]):
                print("point x coord is too far left")
            if(camera.bounds[1] < self.SCpos[0]):
                print("point x coord is too far right")
            if(camera.bounds[2] > self.SCpos[1]):
                print("point y coord is too high")
            if(camera.bounds[3] < self.SCpos[1]):
                print("point y coord is too low")
            if(self.SCpos[2] < 1):
                print("Point is behind camera")
                '''
            
            
            
            
            
            self.outOfShot = True
        else:
            self.outOfShot = False
    

    def updatePosAndRot(self, triangle):

        self.pos = triangle.pos + self.relPos
        self.rotation = triangle.rotation



class lightSource:
    def __init__(self, motionInfo, brightness) -> None:    #   brightness scale is from 1-100
        self.pos = motionInfo[0]
        self.brightness = brightness

        self.vel = motionInfo[1]
        self.acc = motionInfo[2]
    
    def updatePos(self):
        self.vel += self.acc
        self.pos += self.vel



class Camera:
    def __init__(self, pos, rotation, FoVangle) -> None:
        self.pos = pos
        self.xRot = rotation[0]
        self.yRot = rotation[1]
        self.zRot = rotation[2]
        self.updateRotQuat()    #   Gets Rotation quaternion
        self.FoV = math.radians(FoVangle/2)   #   FoV measures the angle of sight to each side, so is halved
        self.bounds = np.array((-40, width+40, -30, height+30))

        self.vel = np.array((0., 0., 0.))
        self.acc = np.array((0, 0, 0))

    def updateRotQuat(self):
        #print("Getting camera rotation")
        #print(f"xRot for rotation quaternion: {self.xRot}")
        rotAxis = np.array(([1, 0, 0], [0, 1, 0], [0, 0, 1]))
        #cameraDefaultRotation = quatFromRotAndAxis(math.pi/2, np.array((0, 1, 0)))
        quatX = quatFromRotAndAxis(self.xRot, (rotAxis[0]))
        quatY = quatFromRotAndAxis(self.yRot, (rotAxis[1]))
        quatZ = quatFromRotAndAxis(self.zRot, (rotAxis[2]))
        #print(f"QuatX: {quatX}\nQuatY: {quatY}\nQuatZ: {quatZ}")
        self.rotQuat = quatX*quatY*quatZ*cameraDefaultRotation
        #print(f"Rotation quaternion from mouse movement: {self.rotQuat}")
        #print(f"RotQuat: {self.rotQuat}")

    def updateMotion(self):
        #print(f"Accel before rotation: {self.acc}\nRotation by {self.rotQuat.conjugate}")
        self.acc = rotateByQuaternion(self.rotQuat, self.acc)
        #print(f"Accel after rotation: {self.acc}")
        self.vel += self.acc
        if(magnitude(self.vel) > maxVelocity):
            self.vel = normalise(self.vel, maxVelocity)
        
        self.pos += self.vel

    def updateRotationInformation(self, rotation):




        
        self.xRot += rotation[0]
        self.yRot += rotation[1]
        self.zRot += rotation[2] 
        #print(f"xRot from mouse movement: {self.xRot}")
        self.updateRotQuat()

    def updateSettings(self, newFoV):
        self.FoV =  math.radians(newFoV/2) 

    def resetPlayerChanges(self):

        self.vel = np.zeros(3)
        self.pos = copy.deepcopy(init_camera_pos)
        self.xRot = init_camera_rotation[0]
        self.yRot = init_camera_rotation[1]
        self.zRot = init_camera_rotation[2]
        self.updateRotQuat()


class vector3:
    def __init__(self, dir) -> None:
        if(dir.shape == 3):
            self.vec = dir
        else:
            print("Incorrect input to vector class! ###############")
            raise TypeError
    
    def normalise(self, scale=1):
        self.vec = scale * (self.vec/self.magnitude())

    def magnitude(self):
        return sum(self.vec*self.vec)







