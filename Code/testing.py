import math
import numpy as np
def rotateByAngle(vector, angle):   #    Clockwise
    # Create the rotation matrix
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ])

    # Rotate the vector
    rotated_vector = np.dot(rotation_matrix, vector)

    return rotated_vector

def getParallelAndPerpendicular(v, y):
    sintheta = dot(normalise(v), y)
    print(sintheta)
    parallel = round(magnitude(v) * sintheta, 6)
    perpendicular = round(magnitude(v) * (math.sqrt(1-sintheta**2)), 6)
    return np.array((parallel, perpendicular))

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



sideRemoval=[0, 1, 0, 0]
print(sideRemoval)
if(sideRemoval.count(0) > 0):
    print("Face is True")






'''
class animal:
    
    def __init__(self) -> None:
        self.alive = True

    def eat(self):
        print("Eating")


class rabbit(animal):
    print(super().__init__())
    self.alive

rabbitName = rabbit()
rabbitName.eat()
'''






'''
class Vertex:
    def __init__(self, x):
        self._x = x
        self._triangle = None

    def getMyPos(self):
        print(self._triangle.pos + self._x)

    @property
    def triangle(self):
        return self._triangle
    
    @triangle.setter
    def triangle(self, value):
        self._triangle = value

class Triangle:
    def __init__(self, vertex1, pos):
        self.vertex1 = vertex1
        self.vertex1.triangle = self
        self.pos = pos

    def getVertexPos(self):
        self.vertex1.getMyPos()

T1 = Triangle(Vertex(-2), (4))
T1.getVertexPos()
T1.pos = 2
T1.getVertexPos()
T1.vertex1._x = 4
T1.getVertexPos()
'''