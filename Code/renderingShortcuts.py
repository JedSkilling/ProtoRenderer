import numpy as np
from classes import *


def makeCuboid(cubeLocation, sideLengths, rotation=quatFromRotAndAxis(0, np.array((1, 0, 0))), scale=1, sideRemoval=[]):  #   Side lengths has each component
    sideLengths *= scale
    #   Cube location in x, y, z

    tmpTriangleList = []
    corners = np.zeros((8, 3))
    
    corners[0] = (0, 0, 0)        #   A 
    corners[1] = (0, 0, sideLengths[2])       #   B

    corners[2] = (0, sideLengths[1], 0)       #   D
    corners[3] = (0, sideLengths[1], sideLengths[2])     #   C

    corners[4] = (0 + sideLengths[0], 0, 0)        #   E
    corners[5] = (0 + sideLengths[0], 0, sideLengths[2])      #   F

    corners[6] = (0 + sideLengths[0], sideLengths[1], 0)      #   H
    corners[7] = (0 + sideLengths[0], sideLengths[1], sideLengths[2])    #   G


    rotQuat = rotation

    for i in range(len(corners)):

        corners[i] = rotateByQuaternion(rotQuat, corners[i])



        #   6/6 sides complete
    face = 1
    if(sideRemoval.count(face) == 0):
        #   Face 1
        T1 = Triangle(cubeLocation, rotation, np.array((corners[3], corners[1], corners[2])))
        T2 = Triangle(cubeLocation, rotation, np.array((corners[2], corners[1], corners[0])))
        tmpTriangleList.append(T1)
        tmpTriangleList.append(T2)

    face+=1

    if(sideRemoval.count(face) == 0):
        #   Face 2
        T3 = Triangle(cubeLocation, rotation, np.array((corners[7], corners[2], corners[6])))
        T4 = Triangle(cubeLocation, rotation, np.array((corners[7], corners[3], corners[2])))
        tmpTriangleList.append(T3)
        tmpTriangleList.append(T4)

    face+=1

    if(sideRemoval.count(face) == 0):
        #   Face 3
        T5 = Triangle(cubeLocation, rotation, np.array((corners[5], corners[6], corners[4])))
        T6 = Triangle(cubeLocation, rotation, np.array((corners[5], corners[7], corners[6])))
        tmpTriangleList.append(T5)
        tmpTriangleList.append(T6)

    face+=1

    if(sideRemoval.count(face) == 0):
        #   Face 4
        T7 = Triangle(cubeLocation, rotation, np.array((corners[1], corners[4], corners[0])))
        T8 = Triangle(cubeLocation, rotation, np.array((corners[1], corners[5], corners[4])))
        tmpTriangleList.append(T7)
        tmpTriangleList.append(T8)

    face+=1

    if(sideRemoval.count(face) == 0):
        #   Face 5
        T9 = Triangle(cubeLocation, rotation, np.array((corners[5], corners[1], corners[3])))
        T10 = Triangle(cubeLocation, rotation, np.array((corners[5], corners[3], corners[7])))
        tmpTriangleList.append(T9)
        tmpTriangleList.append(T10)

    face+=1

    if(sideRemoval.count(face) == 0):
        #   Face 6
        T11 = Triangle(cubeLocation, rotation, np.array((corners[4], corners[2], corners[0])))
        T12 = Triangle(cubeLocation, rotation, np.array((corners[4], corners[6], corners[2])))
        tmpTriangleList.append(T11)
        tmpTriangleList.append(T12)

    return tmpTriangleList


def makeRectangle(center, corners, sideLengths): #   SideLengths has x, y and z
    pass