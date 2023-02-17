import numpy as np
import pygame
import time
import math

class box:
    def __init__(self, motionInfo, mass = 50) -> None:
        self.pos = motionInfo[0]
        self.vel = motionInfo[1]
        self.acc = motionInfo[2]

        self.mass = mass

        self.color = np.array((135, 206, 235))
        
        self.width = 30
        self.height = 30

    def drawSelf(self):
        print(self.pos)
        c1 = self.pos[0]
        c2 = self.pos[1]
        c3 = self.width
        c4 = self.height


        rectInfo = [c1, c2, c3, c4]
        print(rectInfo)
        pygame.draw.rect(surface_main, self.color, rectInfo)

    def updatePos(self):
        self.vel += self.acc
        self.pos += self.vel

    def applyForce(self, force, time=1/30):
        impulse = force * time
        self.vel[0] = impulse[0]/self.mass + self.vel[0]
        self.vel[1] = impulse[1]/self.mass + self.vel[1]

    def checkIntersection(self, testLine):
        xyVals = [self.pos[0], self.pos[0] + self.width, self.pos[1], self.pos[1] + self.height]
        #colliding = False
        xVals = xyVals[:2]
        yVals = xyVals[2:]
        print(f"yVals: {yVals}")
        #   Check rightmost edge for collision
        #   x = self.pos[0] + width
        collX = False
        collY = False
        x = self.pos[0] + self.width
        a = testLine.normal[0]
        b = testLine.normal[1]

        x_1, y_1 = testLine.v1
        x_2, y_2 = testLine.v2

        for x in xVals:
            yIntercept = -(a/b) * (x - x_1) + y_1
            if((0 < yIntercept - self.pos[1] and yIntercept - self.pos[1] < self.height) and (0 < x - x_1 and x - x_1 < (x_2-x_1))):
                print("Colliding with x edge")
                collX = True
        
        for y in yVals:
            xIntercept = -(b/a) * (y - y_1) + x_1
            if((0 < xIntercept - self.pos[0] and xIntercept - self.pos[0] < self.width) and (0 < y - min(y_1, y_2) and (y - min(y_1, y_2)) < abs(y_2 - y_1))):
                print("Colliding with y edge")
                collY = True


        


        print("Coll check finished")
        if(collX or collY):
            self.color = np.array((200, 40, 40))
            self.applyForce(testLine.getForceVector())
        else:
            self.color = np.array((135, 206, 235))
        #print(x, yIntercept, self.pos[1])


        '''
        collX = False
        collY = False
        for i in range(4):
            checkingVal = xyVals[i]
            if(i < 2):
                if(checkingVal > min(testLine.v1[0], testLine.v2[0]) and checkingVal < max(testLine.v1[0], testLine.v2[0])):
                    newy = (testLine.normal[0]/testLine.normal[1])*(testLine.v1[0] - checkingVal) + testLine.v1[1]
                    if(newy > self.pos[1] and newy < self.pos[1] + height):
                        print(checkingVal)
                        collX = True
            else:
                if(checkingVal > min(testLine.v1[1], testLine.v2[1]) and checkingVal < max(testLine.v1[1], testLine.v2[1])):
                    newx = (testLine.normal[1]/testLine.normal[0])*(testLine.v1[1] - checkingVal) + testLine.v1[0]
                    if(newx > self.pos[0] and newx < self.pos[0] + width):
                        print(checkingVal)
                        collY = True
        if(collX and collY):
            self.color = np.array((200, 40, 40))
        else:
            self.color = np.array((135, 206, 235))
        '''            

class line:
    def __init__(self, v1, v2, k, D, width = 4 ) -> None: #   v1,v2 are numpy arrays, k is stiffness, D is dampening
        self.v1 = v1
        self.v2 = v2
        self.k = k
        self.D = D
        self.getNormal()

        self.color = np.array((80, 50, 150))
        self.width = width
        
    def getNormal(self):
        self.normal = normalise(rotateByAngle(self.v2-self.v1, -math.pi/2))
        print(self.normal)

    def drawSelf(self):
        pygame.draw.line(surface_main, self.color, self.v1, self.v2, self.width)

    def getForceVector(self):
        vector = 30*self.k*self.normal
        return vector


def rotateByAngle(vector, angle):
    # Create the rotation matrix
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ])

    # Rotate the vector
    rotated_vector = np.dot(rotation_matrix, vector)

    return rotated_vector

def setup_ui():
    surface_main.fill(background_color)


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

#   Variables
background_color = np.array((30, 20, 40))





pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screenWidth = screen.get_width()
screenHeight = screen.get_height()

surface_main = pygame.Surface((screenWidth,screenHeight))


pygame.display.set_caption("2D Collision")


clock = pygame.time.Clock()

motionInfo = [np.array((500, 660), float), np.array((2, 0), float),  np.array((0, 0.01), float)]
mainBox = box(motionInfo)
mainLine = line(np.array((700, 700)), np.array((1000, 600)), 1, 0)

t=0
running = True
while running:
    setup_ui()
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                mainBox.pos = np.array(mouse, float)
                mainBox.vel = np.array((3, 0), float)



    mainBox.updatePos()

    mainBox.checkIntersection(mainLine)

    mainLine.drawSelf()

    mainBox.drawSelf()

    




    screen.blit(surface_main, (0, 0))

    pygame.display.update()
    clock.tick(30)
    t=t+1