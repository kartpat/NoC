import rhinoscriptsyntax as rs 
import math
import random



arrPoints = list()
for t in rs.frange(-100,100,2):
	x0 = t*math.sin(t)
	y0 = t*math.cos(t)
	z0 = t
	arrPoint = [x0, y0, z0]
    # print(arrPoint)
	arrPoints.append(arrPoint)

print(arrPoints)
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
        self.location = [random.randrange(-300,300,1),random.randrange(-300,300,1),0]
        self.velocity = [random.randrange(-8,8,1),random.randrange(-8,8,1),0]
        self.acceleration = [0,0,0]
        self.listPoints = list()
        self.basePoint = [0,0,0]
        self.vecVelocity = rs.VectorCreate(self.velocity, self.basePoint)
        self.vecAcceleration = [0,0,0]
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
class Attractor(object):

    def __init__(self):
        self.location = [0,0,0]
        self.velocity = [0,.2,.1]
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
        forceMag = limit(forceMag,2.0 , 27.0)
        forceDir = rs.VectorUnitize(forceDir)
        # print forceDir
        strength = (self.g*self.mass)/(forceMag*forceMag)
        # strength = limit(strength,1,15)
        # print strength
        finalForce = rs.VectorScale(forceDir,strength)
        return finalForce


m = Mover() 
a = Attractor()



for x in rs.frange(0, 2000, 1):

    attraction = a.attract(m)
    a.update()
    # print attraction
    # print m.vecAcceleration
    m.applyForce(attraction)
    # m.applyForce([0,.1,.1])
    m.update()
    m.display()
    # rs.AddPoint(m.location)

# print m.location[0]
# print m.listPoints
rs.AddInterpCurve(m.listPoints)
# rs.AddPoint(m.listPoints)
