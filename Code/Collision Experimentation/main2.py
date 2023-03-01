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

    def applyImpulse(self, force, time=1/30):
        impulse = force * time
        self.vel[0] = impulse[0]/self.mass + self.vel[0]
        self.vel[1] = impulse[1]/self.mass + self.vel[1]

    def checkIntersection(self, testLine):

        #   The top left and top right corners of the box
        xVals = [self.pos[0], self.pos[0] + self.width]
        yVals = [self.pos[1], self.pos[1] + self.height]

        #   Check rightmost edge for collision
        collX = False
        collY = False

        #   Setting up variables for calculation
        x = self.pos[0] + self.width
        a = testLine.normal[0]
        b = testLine.normal[1]

        x_1, y_1 = testLine.v1
        x_2, y_2 = testLine.v2

        for x in xVals:
            yIntercept = -(a/b) * (x - x_1) + y_1
            #   First check is if if the y intercept falls in the y bounds of the collision, second check checks if the initial x values fall in x bounds of collision
            relativeYPos = yIntercept - self.pos[1]
            relativeXPos = x - x_1
            if((0 < relativeYPos and relativeYPos < self.height) and (0 < relativeXPos and relativeXPos < (x_2-x_1))):
                print("Colliding with x edge")
                collX = True
        
        for y in yVals:
            xIntercept = -(b/a) * (y - y_1) + x_1
            relativeXPos = xIntercept - self.pos[0]
            relativeYPos = y - min(y_1, y_2)
            if((0 < relativeXPos and relativeXPos < self.width) and (0 < relativeYPos and relativeYPos < abs(y_2 - y_1))):
                print("Colliding with y edge")
                collY = True


        print("Coll check finished")
        if(collX or collY):
            self.actionOnIntersection(testLine)
        else:
            self.color = np.array((135, 206, 235))

    def actionOnIntersection(self, testLine):
        if(instantReactionImpulse):
            if(dot(self.vel, testLine.normal) < 0):
                self.calcReactionImpulse(testLine)
        else:
            self.gradualForceIntersection(testLine)
        self.gradualForceIntersection(testLine, 0.0001)


    def gradualForceIntersection(self, testLine, magnitude=1):
        self.color = np.array((200, 40, 40))
        if(dot(self.vel, testLine.normal) > 0):
            currentRestitionVal = testLine.restitution
        else:
            currentRestitionVal = 1

        self.applyImpulse(magnitude*currentRestitionVal * testLine.getForceVector())
        self.vel -= self.acc * currentRestitionVal

    def calcReactionImpulse(self, testLine):    #   Assumptions: 1. Testline is stationary, so we are already in its reference frame 2. restitution num is the value for the moving object
        #   For new reference frame with will change
        relVel1 = getParallelAndPerpendicular(self.vel, testLine.normal)

        m1 = self.mass
        m2 = testLine.mass
        v1 = relVel1[0]
        restitution = testLine.restitution
        if(m2 == -1):   #   For case of an object that won't move (ie the equations as mass 2 tends to infinity)
            u1 = -v1*restitution
            u2 = 0
        else:
            mCombo = (m1/restitution)-m2
            if(mCombo == 0):
                u1 = 0
                u2 = v1*restitution
            else:
                u1 = v1 * mCombo *restitution / (m1 + m2)
                u2 = (v1*restitution) + u1

        #   For new reference frame with will change
        deltaV1 = u1 - v1
        deltaV2 = u2
        impulse1 = deltaV1*m1
        self.applyImpulse(impulse1*testLine.normal, 1)
        if(not testLine.mass == -1):
            impulse2 = deltaV2*m2
            #testLine.applyImpulse()    Not implemented yet
            NotImplementedError



    def getKE(self):
        KE = 1/2 * self.mass * magnitude(self.vel)**2
        return KE


    def getGPE(self):
        GPE = self.mass * gravityStrength * (screenHeight - self.pos[1])
        return GPE

    def getMomentum(self):
        momentum = self.mass * magnitude(self.vel)
        return momentum




class line:
    def __init__(self, v1, v2, stiffness, restitution, width = 4, mass = -1) -> None: #   v1,v2 are numpy arrays, restitution is effectively dampening
        self.v1 = v1
        self.v2 = v2
        self.stiffness = stiffness
        self.restitution = restitution
        self.mass = mass
        self.getNormal()

        self.color = np.array((80, 50, 150))
        self.width = width
        
    def getNormal(self):
        self.normal = normalise(rotateByAngle(self.v2-self.v1, -math.pi/2))
        print(self.normal)

    def drawSelf(self):
        pygame.draw.line(surface_main, self.color, self.v1, self.v2, self.width)

    def getForceVector(self):
        vector = 30*self.stiffness*self.normal
        return vector


def rotateByAngle(vector, angle):   #    Clockwise
    # Create the rotation matrix
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ])

    # Rotate the vector
    rotated_vector = np.dot(rotation_matrix, vector)

    return rotated_vector

def getParallelAndPerpendicular(v, y):  #   Returns two values corresponding to the vector in parallel/perpendicular base coords
    sintheta = dot(normalise(v), y)
    print(sintheta)
    parallel = round(magnitude(v) * sintheta, 6)
    perpendicular = round(magnitude(v) * (math.sqrt(1-sintheta**2)), 6)
    return np.array((parallel, perpendicular))


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

gravityStrength = 0.01
instantReactionImpulse = True


pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screenWidth = screen.get_width()
screenHeight = screen.get_height()

surface_main = pygame.Surface((screenWidth,screenHeight))


pygame.display.set_caption("2D Collision")


clock = pygame.time.Clock()

allLines = []

motionInfo = [np.array((500, 660), float), np.array((2, 0), float),  np.array((0, 0.01), float)]
mainBox = box(motionInfo)
line01 = line(np.array((400, 700)), np.array((1000, 700)), 10, 0.9)
allLines.append(line01)

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
                mainBox.vel = np.array((0, 0), float)


    mainBox.updatePos()
    
    for singleLine in allLines:
        mainBox.checkIntersection(singleLine)

    




    for singleLine in allLines:
        singleLine.drawSelf()

    mainBox.drawSelf()

    # region : Writing Info To Screen
    smallfont = pygame.font.SysFont('Corbel',15)
    
    mouseInfo = f"Mouse Movement: {mouse}"
    boxPos = f"Pos: {mainBox.pos}"
    boxVel = f"Vel: {mainBox.vel}"
    boxAcc = f"Acc: {mainBox.acc}"
    timeInfo = f"t:{t}"
    KE = round(mainBox.getKE()) #   These are rounded, avoid doing calculations with them
    GPE = round(mainBox.getGPE())
    boxKE = f"Kinetic Energy:{KE}"
    boxGPE = f"Gravitional Potential:{GPE}"
    boxTotalEnergy = f"Total Energy:{KE+GPE}"

    

    mouseText = smallfont.render(mouseInfo, True , (255,255,255))
    camPosText = smallfont.render(boxPos, True, (255, 255, 255))
    camVelText = smallfont.render(boxVel, True, (255, 255, 255))
    camAccText = smallfont.render(boxAcc, True, (255, 255, 255))

    boxKEText = smallfont.render(boxKE, True, (255, 255, 255))
    boxGPEText = smallfont.render(boxGPE, True, (255, 255, 255))
    boxTotalEnergyText = smallfont.render(boxTotalEnergy, True, (255, 255, 255))
    timeText = smallfont.render(timeInfo, True , (255,255,255))
    # endregion
    
    #   Game blits
    screen.blit(surface_main, (0, 0))

    

    # region : Info blits

    pygame.draw.rect(screen,(140,140,150),[0,0,180,120])
    firstColumn = 10
    screen.blit(mouseText, (firstColumn,10))
    screen.blit(camPosText, (firstColumn, 25))
    screen.blit(camVelText, (firstColumn, 40))
    screen.blit(camAccText, (firstColumn, 55))
    screen.blit(timeText, (firstColumn, 70))

    pygame.draw.rect(screen,(120,120,125),[180,0,360,60])
    secondColumn = 190
    screen.blit(boxKEText, (secondColumn, 10))
    screen.blit(boxGPEText, (secondColumn, 25))
    screen.blit(boxTotalEnergyText, (secondColumn, 40))

    

    # endregion






    pygame.display.update()
    clock.tick(30)
    t=t+1