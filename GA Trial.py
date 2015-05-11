import rhinoscriptsyntax as rs 
import math
import random



# arrPoints = list()
# for t in rs.frange(-100,100,2):
# 	x0 = t*math.sin(t)
# 	y0 = t*math.cos(t)
# 	z0 = t
# 	arrPoint = [x0, y0, z0]
#     # print(arrPoint)
# 	arrPoints.append(arrPoint)

# print(arrPoints)
# rs.AddPoint(arrPoint) #Call rs.EnableRedraw(True)

# rs.AddInterpCurve(arrPoints)	

def limit(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n

class Mover(object):

    def __init__(self):
        self.location = [random.randrange(-300,300,1),random.randrange(-300,300,1),random.randrange(-300,300,1)]
        # self.velocity = [random.randrange(-8,8,1),random.randrange(-8,8,1),random.randrange(-8,8,1)]
        self.velocity = [0,0,0]
        self.acceleration = [0,0,0]
        self.listPoints = list()
        self.basePoint = [0,0,0]
        self.vecVelocity = rs.VectorCreate(self.velocity, self.basePoint)
        self.vecAcceleration = [0,0,0]
        self.g = 0.4
        self.mass = 1
        # self.topspeed = 10

    def update(self):
        
        self.vecAcceleration = rs.VectorCreate(self.acceleration, self.basePoint)    
        self.vecVelocity = rs.VectorAdd(self.vecVelocity,self.vecAcceleration)
        self.location = rs.PointAdd(self.location,self.vecVelocity)
        self.acceleration = rs.VectorScale(self.acceleration,0)

    def display(self):
        tmpLoc = (self.location[0],self.location[1],self.location[2])
        # print tmpLoc
        self.listPoints.append(tmpLoc)

    def applyForce(self,receivedForce):
        vecForce = rs.VectorCreate(receivedForce, self.basePoint)
        # print vecForce
        self.acceleration = rs.VectorAdd(self.acceleration, vecForce)
        # print self.acceleration

    def attract(self,mover):
        forceDir = rs.VectorSubtract(self.location,mover.location)
        forceMag = rs.Distance(self.location,mover.location)
        # forceMag = limit(forceMag,2.0 , 27.0)
        # forceDir = rs.VectorUnitize(forceDir)
        # print forceDir
        strength = (self.g*self.mass)/(forceMag*forceMag*forceMag + 100.0)
        # strength = limit(strength,1,15)
        # print strength
        finalForce = rs.VectorScale(forceDir,strength)
        return [-finalForce[1],finalForce[0],finalForce[2]]
        # return finalForce

class Attractor(object):

    def __init__(self):
        self.location = [0,0,0]
        self.velocity = [0,.1,.1]
        self.acceleration = [0,0,0]
        self.basePoint = [0,0,0]
        self.vecAcceleration = rs.VectorCreate(self.acceleration, self.basePoint)
        self.vecVelocity = rs.VectorCreate(self.velocity, self.basePoint) 
        self.mass = 2000
        self.g = 0.4

    def update(self):
           
        self.vecVelocity = rs.VectorAdd(self.vecVelocity,self.vecAcceleration)
        self.location = rs.PointAdd(self.location,self.vecVelocity)
        # self.acceleration = rs.VectorScale(self.acceleration,0)

    def attract(self,mover):
        forceDir = rs.VectorSubtract(self.location,mover.location)
        forceMag = rs.Distance(self.location,mover.location)
        # forceMag = limit(forceMag,2.0 , 27.0)
        # forceDir = rs.VectorUnitize(forceDir)
        # print forceDir
        strength = (self.g*self.mass)/(forceMag*forceMag + 10.0)
        # strength = limit(strength,1,15)
        # print strength
        finalForce = rs.VectorScale(forceDir,strength)
        return [-finalForce[1],finalForce[0],finalForce[2]]


moverList = []

for i in range(100):
    moverList.append(Mover())

# a = Attractor()

# THE BELOW FUNCTION SIMULATES THE DRAW LOOP IN PROCESSING

for x in range(0, 15000, 5):

    for n1 in range(len(moverList)):
        for n2 in range(len(moverList)): 
            if n1 != n2:
                attraction = moverList[n2].attract(moverList[n1])
                # a.update()
                # print attraction[0]
                # print m.vecAcceleration
                moverList[n1].applyForce(attraction)
                # moverList[n].applyForce([0,.1,.1])
        moverList[n1].update()
        moverList[n1].display()
                # rs.AddPoint(m.location)

# print m.location[0]
# print m.listPoints
for p in range(len(moverList)):
    rs.AddInterpCurve(moverList[p].listPoints)

# rs.AddPoint(m.listPoints)


class DNA(object):

    def __init__(self):
        self.genes = list()
        
