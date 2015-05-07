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
		self.stiffnessOn()
		self.postureProxy.goToPosture("StandInit", 0.5)
		self.motionProxy.setWalkArmsEnabled(True, True)
		self.motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
		X = 0.5  
		Y = 0.0
		Theta = 0.0
		Frequency =0.0 # low speed
		self.motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

	def turnRightRad(self,rad):
		self.stopWalking()
		x=0.0
		y=0.0
		theta=rad
		self.motionProxy.moveTo(x, y, theta)

	def turnLeftRad(self,rad):
		self.stopWalking()
		x=0.0
		y=0.0
		theta=-rad
		self.motionProxy.moveTo(x, y, theta)

	def moveLeft(self):
		self.stopWalking()
		self.stiffnessOn()
		self.postureProxy.goToPosture("StandInit", 0.5)
		self.motionProxy.setWalkArmsEnabled(True, True)
		X = 0.2  
		Y = -0.5
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

