import rhinoscriptsyntax as rs 
import math
import random

def mapRange(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class DNA(object):
	def __init__(self):
		self.gene = [random.randrange(-300,300,1),random.randrange(-300,300,1),random.randrange(-300,300,1)]
		self.fitness = 0

	def fitness(self, targetLoc):
		dist = rs.Distance(self.gene, targetLoc)
		self.fitness = 1.0 / (1.0 + dist)

	def crossover(self, partner):
		child = DNA()
		child.gene[0] = (self.gene[0] + partner.gene[0]) / 2.0
		child.gene[1] = (self.gene[1] + partner.gene[1]) / 2.0
		child.gene[2] = (self.gene[2] + partner.gene[2]) / 2.0
		return child

	def mutate(self,mutation):
		if random.random() < mutation:
			self.gene = [random.randrange(-300,300,1),random.randrange(-300,300,1),random.randrange(-300,300,1)]

class Population(object):
	def __init__(self, t, m ,n):

		self.targetLoc = t;
		self.mutationRate = m
		self.pop = []
		for i in range(n):
			self.pop.append(DNA())

		self.calcFitness()
		self.matingPool = list()
		self.finished = false
		self.generation = 0
		self.perfectScore = 1

	def calcFitness(self):
		for x in range(len(self.pop)):
			# check if self needs to be removed from below
			self.pop[x].fitness(self.targetLoc)

	def naturalSelection(self):
		self.matingPool = []
		maxFitness = 0
		for i in range(len(self.pop)):
			if self.pop[i].fitness > maxFitness:
				maxFitness = self.pop[i].fitness

		for j in range(len(self.pop)):
			fit = mapRange(self.pop[j].fitness, 0, maxFitness , 0,1)
			n = int(fit*100)
			for k in range(n):
				self.matingPool.append(self.pop[j])

	def generate(self):
		for i in range(len(self.pop)):
			a = int(random.random(len(self.matingPool)))
			b = int(random.random(len(self.matingPool)))
			# get function of the python - change it after reference
			partnerA = 	self.matingPool[a]
			partnerB = 	self.matingPool[b]
			child = partnerA.crossover(partnerB)
			child.mutate(self.mutation)
		self.generation = self.generation+1

	def getBest(self):
		worldRecord = 0.0
		index = 0
		for i in range(len(self.pop)):
			if self.pop[i].fitness > worldRecord:
				index = i
				worldRecord = self.pop[i].fitness
		if worldRecord == self.perfectScore:
			self.finished = true
		return self.pop[index].gene	

	def finished(self):
		return self.finished

	def generations():
		return self.generations

pointList = []
target = [250,250,250]
mutationRate = 0.01
popMax = 50

popul = Population(target,mutationRate, popMax)

# The fucntion below simlates the Draw loop in processing

for x in range(5000):
	
	popul.naturalSelection()
	popul.generate()
	popul.calcFitness()
	answer = popul.getBest()
	rs.AddPoint(answer)
	if popul.finished():
		print "Its all done."

#     for n1 in range(len(moverList)):
#         for n2 in range(len(moverList)): 
#             if n1 != n2:
#                 attraction = moverList[n2].attract(moverList[n1])
#                 # a.update()
#                 # print attraction[0]
#                 # print m.vecAcceleration
#                 moverList[n1].applyForce(attraction)
#                 # moverList[n].applyForce([0,.1,.1])
#         moverList[n1].update()
#         moverList[n1].display()
#                 # rs.AddPoint(m.location)

# # print m.location[0]
# # print m.listPoints
# for p in range(len(moverList)):
#     rs.AddInterpCurve(moverList[p].listPoints)

# # rs.AddPoint(m.listPoints)





