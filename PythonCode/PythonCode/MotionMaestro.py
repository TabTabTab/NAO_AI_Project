from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import time

class MotionMaestro:

	def __init__(self,postureProxy,motionProxy):
		self.postureProxy=postureProxy
		self.motionProxy=motionProxy		

	def standUp(self):
		print "Standing Up"
		self.postureProxy.goToPosture("Stand", 1.0)

	def sitDown(self):
		print "Sitting Down"
		self.postureProxy.goToPosture("Sit", 1.0)

	def startWalking(self):
		self.move(0.5,0.0)

	def continueStraight(self):
		X=0.8
		Y=0
		Theta = 0.0
		Frequency =0.0 # low speed
		self.motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
	def turnRightRad(self,theta):
		self.turnRad(-theta)

	def turnLeftRad(self,theta):
		self.turnRad(theta)

	#pos theta is left neg is right
	def turnRad(self,theta):
		self.stopWalking()
		x=0.0
		y=0.0
		self.motionProxy.moveTo(x, y, theta)


	def moveLeft(self):
		self.move(0.0,0.5)

	def moveRight(self):
		self.move(0.0,-0.5)

	def move(self,X,Y):
		self.stopWalking()
		self.stiffnessOn()
		self.postureProxy.goToPosture("StandInit", 0.5)
		self.motionProxy.setWalkArmsEnabled(True, True)
		#X = 0.0  
		#Y = 0.5
		Theta = 0.0
		Frequency =0.0 # low speed
		self.motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)


	def stopWalking(self):
		X = 0.0
		Y = 0.0
		Theta = 0.0
		Frequency =1.0
		self.motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)


	def stiffnessOn(self):
		pNames = "Body"
		pStiffnessLists = 1.0
		pTimeLists = 1.0
		self.motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

