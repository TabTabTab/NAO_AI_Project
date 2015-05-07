from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import time

def standUp(postureProxy):
	print "Standing Up"
	postureProxy.goToPosture("Stand", 1.0)

def sitDown(postureProxy):
	print "Sitting Down"
	postureProxy.goToPosture("Sit", 1.0)

def startWalking(postureProxy,motionProxy):
	stiffnessOn(motionProxy)
	postureProxy.goToPosture("StandInit", 0.5)
	motionProxy.setWalkArmsEnabled(True, True)
	motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
	X = 0.5  
	Y = 0.0
	Theta = 0.0
	Frequency =0.0 # low speed
	motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def turnRight(postureProxy,motionProxy):
	stopWalking(motionProxy)
	stiffnessOn(motionProxy)
	postureProxy.goToPosture("StandInit", 0.5)
	motionProxy.setWalkArmsEnabled(True, True)
	X = 0.0  
	Y = -0.0
	Theta = -0.5
	Frequency =0.0 # low speed
	motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)




def turnRight2(motionProxy):
	motionProxy.setStiffnesses("HeadYaw",0)
	motionProxy.setAngles("HeadYaw",-0.5,0.05)
	motionProxy.setStiffnesses("HeadYaw",1)
	time.sleep(5)


def turnRight3(motionProxy):
	x=0.0
	y=0.0
	theta=1.5709
	motionProxy.moveTo(x, y, theta)

def turnRightRad(motionProxy,rad):
	x=0.0
	y=0.0
	theta=rad
	motionProxy.moveTo(x, y, theta)

def turnLeftRad(motionProxy,rad):
	x=0.0
	y=0.0
	theta=-rad
	motionProxy.moveTo(x, y, theta)

def turnLeft(postureProxy,motionProxy):
	stopWalking(motionProxy)
	stiffnessOn(motionProxy)
	postureProxy.goToPosture("StandInit", 0.5)
	motionProxy.setWalkArmsEnabled(True, True)
	X = 0.2  
	Y = -0.5
	Theta = 0.0
	Frequency =0.0 # low speed
	motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)





def stopWalking(motionProxy):
    X = 0.0
    Y = 0.0
    Theta = 0.0
    Frequency =1.0
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def stiffnessOn(motionProxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)