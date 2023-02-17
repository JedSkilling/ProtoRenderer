import numpy as np
from pyquaternion import Quaternion as quaternion
import math
from settings import *


from pygameInit import *

#   General
def quatFromRotAndAxis(Rot, axis):
    axis=normalise(axis)
    newAxis = math.sin(Rot/2)*axis
    q1 = quaternion(math.cos(Rot/2), newAxis[0], newAxis[1], newAxis[2])
    return q1

def rotateByQuaternion(rotationQuaternion, inputVector):
    if(inputVector.any() == 0):
        #print("Input is all 0")
        return inputVector
    inputVectorMagnitude = sum(inputVector*inputVector)
    inputVectorNormalised = inputVector/inputVectorMagnitude
    inputVectorQuaternion = rotationQuaternion*quaternion(0, inputVectorNormalised[0], inputVectorNormalised[1], inputVectorNormalised[2])*rotationQuaternion.conjugate
    outVector = inputVectorMagnitude*np.array((inputVectorQuaternion.x, inputVectorQuaternion.y, inputVectorQuaternion.z))
    return outVector

def cross(v1, v2):
    v3 = np.zeros(3)
    v3[0] = v1[1]*v2[2]-v1[2]*v2[1]
    v3[1] = v1[2]*v2[0]-v1[0]*v2[2]
    v3[2] = v1[0]*v2[1]-v1[1]*v2[0]
    return v3

def dot(v1, v2):
    mag = sum(v1*v2)
    return mag
def mean3(a, b, c):
    d = (a+b+c)/3
    return d
def normalise(vector, scale=1):
    if(magnitude(vector) == 0):
        return vector
    return scale * (vector/magnitude(vector))

def magnitude(vector):
    return math.sqrt(sum(vector*vector))


#   Project specific parts


def SCtoActualCoord(SCinput):
    v1 = np.zeros(2)
    v1[0] = (width/2)*SCinput[1]+width/2
    v1[1] = (width/2)*SCinput[0]+height/2
    return v1

def getSortVal(input):
        return input[4]