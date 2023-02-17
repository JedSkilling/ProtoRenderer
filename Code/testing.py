import numpy as np
class vector3:
    def __init__(self, dir) -> None:
        
        self.vec = dir

    
    def normalise(self, scale=1):
        self.vec = scale * (self.vec/self.magnitude())

    def magnitude(self):
        return sum(self.vec*self.vec)

v1 = vector3(np.array((1, 2, 3)))
print(v1.magnitude())
v1.normalise()
print(v1.vec)













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